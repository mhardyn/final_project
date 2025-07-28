import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')
django.setup()

from django.contrib.auth.models import User

CSV_PATH = 'employee_management_system/migrations/employees.csv'

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    created_count = 0
    for row in reader:
        pesel = row['pesel'].strip()
        first_name = row['name'].strip()
        last_name = row['surname'].strip()

        if not pesel:
            print("⚠️ The line without PESEL was skipped:", row)
            continue

        if not User.objects.filter(username=pesel).exists():
            user = User.objects.create_user(
                username=pesel,
                password='haslo123',
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            print(f"✅ User created: {pesel} - {first_name} {last_name}")
            created_count += 1
        else:
            print(f"ℹ️ User {pesel} already exists")

print(f"\n🏁 Completed. {created_count} new users created.")
