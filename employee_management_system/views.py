import json
from datetime import date, datetime as dt
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .utils import write_employees_to_csv
from .models import Holiday, Employee


def all_employees(request):
    employees = Employee.objects.all()
    return render(request, 'employee_management_system/employee_all.html', {'employees': employees})


def employee_detail(request, pesel):
    employee = get_object_or_404(Employee, pesel=pesel)
    return render(request, 'employee_management_system/employee_details.html', {'employee': employee})


def employee_search(request):
    employee = None
    error = None
    if request.method == 'POST':
        pesel = request.POST.get('pesel')
        try:
            employee = Employee.objects.get(pesel=pesel)
        except Employee.DoesNotExist:
            error = "No employee with the given PESEL number was found."
    return render(request, 'employee_management_system/employee_search.html', {'employee': employee, 'error': error})


def holidays_view(request):
    employees = Employee.objects.all()
    current_year = date.today().year
    remaining = {}

    for emp in employees:
        try:
            user = User.objects.get(username=emp.pesel)
            taken = Holiday.objects.filter(employee=user, date__year=current_year).count()
            remaining[emp.pesel] = 26 - taken
        except User.DoesNotExist:
            remaining[emp.pesel] = 'No account'

    return render(request, 'employee_management_system/holidays.html', {
        'employees': employees,
        'remaining': remaining,
        'current_year': current_year
    })

def holidays_events_json(request):
    current_year = date.today().year
    holidays = Holiday.objects.filter(date__year=current_year)
    data = [{
        'title': h.employee.get_full_name() or h.employee.username,
        'start': h.date.isoformat(),
        'allDay': True
    } for h in holidays]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def add_holiday(request):
    data = json.loads(request.body)
    date_str = data.get('date')
    pesel = data.get('employee_info')
    if not date_str or not pesel:
        return JsonResponse({'success': False, 'message': 'No data'})
    try:
        date_obj = dt.strptime(date_str, "%Y-%m-%d").date()
        user = User.objects.get(username=pesel)
    except (ValueError, User.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'User not found or invalid date'})

    year = date_obj.year
    if Holiday.objects.filter(employee=user, date=date_obj).exists():
        return JsonResponse({'success': False, 'message': 'Vacation already exists'})
    if Holiday.objects.filter(date=date_obj).count() >= 5:
        return JsonResponse({'success': False, 'message': 'As of today, there are already 5 people on leave'})
    if Holiday.objects.filter(employee=user, date__year=year).count() >= 26:
        return JsonResponse({'success': False, 'message': 'The employee used 26 days of leave this year'})

    Holiday.objects.create(employee=user, date=date_obj)
    return JsonResponse({'success': True})


@csrf_exempt
@require_POST
def delete_holiday(request):
    data = json.loads(request.body)
    date_str = data.get('date')
    pesel = data.get('employee_info')

    if not date_str or not pesel:
        return JsonResponse({'success': False, 'message': 'Data error'})

    try:
        date_obj = dt.strptime(date_str, "%Y-%m-%d").date()
        user = User.objects.get(username=pesel)
    except (ValueError, User.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Data error'})

    deleted, _ = Holiday.objects.filter(employee=user, date=date_obj).delete()
    if deleted:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Vacation not found'})


def get_remaining_days(request):
    current_year = date.today().year
    data = []
    for user in User.objects.exclude(username='admin'):
        taken = Holiday.objects.filter(employee=user, date__year=current_year).count()
        data.append({
            'pesel': user.username,
            'name': f"{user.first_name} {user.last_name}".strip(),
            'remaining_days': 26 - taken
        })
    return JsonResponse(data, safe=False)


def get_birth_date_from_pesel(pesel):
    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if 1 <= month <= 12:
        century = 1900
    elif 21 <= month <= 32:
        century = 2000
        month -= 20
    elif 41 <= month <= 52:
        century = 2100
        month -= 40
    elif 61 <= month <= 72:
        century = 2200
        month -= 60
    elif 81 <= month <= 92:
        century = 1800
        month -= 80
    else:
        raise ValueError("Incorrect month in PESEL")

    full_year = century + year
    return date(full_year, month, day)


def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def statistics(request):
    employees = Employee.objects.all()
    if not employees.exists():
        return render(request, 'employee_management_system/statistics.html', {
            'employee_count': 0,
            'total_salary': 0,
            'min_salary': 0,
            'max_salary': 0,
            'average_salary': 0,
            'average_age': 0,
        })

    employee_count = employees.count()
    salaries = employees.values_list('salary', flat=True)

    ages = []
    for emp in employees:
        try:
            birth_date = get_birth_date_from_pesel(emp.pesel)
            ages.append(calculate_age(birth_date))
        except Exception:
            pass

    total_salary = sum(salaries)
    min_salary = min(salaries)
    max_salary = max(salaries)
    average_salary = total_salary / employee_count
    average_age = round(sum(ages) / len(ages), 1) if ages else 0

    return render(request, 'employee_management_system/statistics.html', {
        'employee_count': employee_count,
        'total_salary': total_salary,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'average_salary': round(average_salary, 2),
        'average_age': average_age,
    })

def employee_edit(request, pesel):
    employee = get_object_or_404(Employee, pesel=pesel)

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        pesel_new = request.POST.get('pesel')
        residential_address = request.POST.get('residential_address')
        date_of_employment = request.POST.get('date_of_employment')
        salary = request.POST.get('salary')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        employee.name = name
        employee.surname = surname
        employee.pesel = pesel_new
        employee.residential_address = residential_address
        employee.date_of_employment = date_of_employment
        employee.salary = salary
        employee.phone_number = phone_number
        employee.email = email
        employee.save()

        try:
            user = User.objects.get(username=pesel)
            if pesel != pesel_new:
                user.username = pesel_new
            user.first_name = name
            user.last_name = surname
            user.email = email
            user.save()
        except User.DoesNotExist:
            User.objects.create_user(
                username=pesel_new,
                password='defaultpassword',
                first_name=name,
                last_name=surname,
                email=email
            )

        write_employees_to_csv()
        return redirect('employee_detail_url', pesel=pesel_new)

    return render(request, 'employee_management_system/employee_edit.html', {'employee': employee})

@require_POST
def delete_employee(request, pesel):
    employee = get_object_or_404(Employee, pesel=pesel)
    employee.delete()

    try:
        user = User.objects.get(username=pesel)
        user.delete()
    except User.DoesNotExist:
        pass

    write_employees_to_csv()
    return redirect('all_employees_url')



def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        pesel = request.POST.get('pesel')
        residential_address = request.POST.get('residential_address')
        date_of_employment = request.POST.get('date_of_employment')
        salary = request.POST.get('salary')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        employee = Employee.objects.create(
            name=name,
            surname=surname,
            pesel=pesel,
            residential_address=residential_address,
            date_of_employment=date_of_employment,
            salary=salary,
            phone_number=phone_number,
            email=email,
        )

        if not User.objects.filter(username=pesel).exists():
            User.objects.create_user(
                username=pesel,
                password='defaultpassword',
                first_name=name,
                last_name=surname,
                email=email,
            )

        write_employees_to_csv()
        return redirect(reverse('all_employees_url'))

    return render(request, 'employee_management_system/employee_add.html')

