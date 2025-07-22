import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from employee_management_system.models import Employee
from django.contrib.auth.models import User
from django.conf import settings
import os


def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Niepoprawny format daty: {date_str}")


class Command(BaseCommand):
    help = 'Importuje pracowników z pliku CSV i tworzy konta użytkowników'

    def handle(self, *args, **kwargs):
        filepath = os.path.join(settings.BASE_DIR, 'employee_management_system/migrations/employees.csv')

        if not os.path.exists(filepath):
            self.stderr.write(self.style.ERROR(f"Plik {filepath} nie istnieje"))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            count = 0
            for row in reader:
                pesel = row['pesel']
                if Employee.objects.filter(pesel=pesel).exists():
                    continue

                try:
                    date_obj = parse_date(row['date_of_employment'])
                except ValueError as e:
                    self.stderr.write(self.style.ERROR(str(e)))
                    continue

                employee = Employee.objects.create(
                    name=row['name'],
                    surname=row['surname'],
                    pesel=pesel,
                    residential_address=row['residential_address'],
                    date_of_employment=date_obj,
                    salary=row['salary'],
                    phone_number=row.get('phone_number') or None,
                    email=row.get('email') or None,
                )

                if not User.objects.filter(username=pesel).exists():
                    User.objects.create_user(
                        username=pesel,
                        password='defaultpassword',
                        first_name=row['name'],
                        last_name=row['surname'],
                        email=row.get('email', '')
                    )

                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Zaimportowano {count} pracowników."))

