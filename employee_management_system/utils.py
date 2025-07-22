import csv
from django.conf import settings
from pathlib import Path

CSV_FILE_PATH = Path(settings.BASE_DIR) / 'employee_management_system' / 'employees.csv'

def write_employees_to_csv():
    from .models import Employee

    fieldnames = [
        'name', 'surname', 'pesel', 'residential_address',
        'date_of_employment', 'salary', 'phone_number', 'email'
    ]

    with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for emp in Employee.objects.all():
            writer.writerow({
                'name': emp.name,
                'surname': emp.surname,
                'pesel': emp.pesel,
                'residential_address': emp.residential_address,
                'date_of_employment': emp.date_of_employment,
                'salary': emp.salary,
                'phone_number': emp.phone_number or '',
                'email': emp.email or '',
            })
