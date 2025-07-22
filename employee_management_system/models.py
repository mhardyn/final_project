import csv
import datetime
from django.db import models
from django.contrib.auth.models import User


def parse_date(date_str):
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Niepoprawny format daty: {date_str}")

class Employees:
    def __init__(self, name, surname, pesel, residential_address, date_of_employment, salary, phone_number, email):
        self.name = name
        self.surname = surname
        self.pesel = pesel
        self.residential_address = residential_address
        self.date_of_employment = parse_date(date_of_employment)
        self.salary = float(salary)
        self.phone_number = phone_number
        self.email = email


    @staticmethod
    def get_all_employees():
        with open('employee_management_system/migrations/employees.csv', 'r', encoding='utf-8') as employees:
            reader = csv.DictReader(employees, delimiter=';')
            return list(map(
                lambda row: Employees(
                    row['name'],
                    row['surname'],
                    row['pesel'],
                    row['residential_address'],
                    row['date_of_employment'],
                    row['salary'],
                    row['phone_number'],
                    row['email'],
                )
            , reader))

    @staticmethod
    def find_by_pesel(pesel):
        with open('employee_management_system/migrations/employees.csv', 'r', encoding='utf-8') as employees:
            reader = csv.DictReader(employees, delimiter=';')
            for row in reader:
                if row['pesel'] == pesel:
                    return Employees(
                        row['name'],
                        row['surname'],
                        row['pesel'],
                        row['residential_address'],
                        row['date_of_employment'],
                        row['salary'],
                        row['phone_number'],
                        row['email'],
                    )


from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    pesel = models.CharField(max_length=11, unique=True)
    residential_address = models.CharField(max_length=255)
    date_of_employment = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Holiday(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.employee.username} - {self.date}"



