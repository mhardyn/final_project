🧑‍💼 Employee and Holiday Management System

## 📋 Project Description

This is a Django-based web application designed for managing employee records and tracking holidays. It allows:

- Managing employee data (add, edit, delete)
- Monitoring employee holidays and remaining leave days
- Generating statistics on salaries and employee ages
- Syncing employee data with a CSV file for bulk import/export

This project is ideal for small to medium-sized companies looking to streamline HR operations.

---

## 🛠️ Features

### 👨‍💼 Employees
- Add, edit, and delete employees
- Search employees by PESEL (Polish national ID number)
- Automatically create and manage corresponding Django user accounts

### 🗓️ Holidays
- Add and delete holiday entries for employees by clicking on specific days
- Each employee can take up to **26 days of holiday per year**
- A maximum of **5 employees can be on holiday on the same day**
- Real-time calculation of remaining leave days per employee

### 📊 Statistics
- View total number of employees
- Calculate total, minimum, maximum, and average salaries
- Calculate average age of employees based on PESEL

### 📁 CSV Integration
- Bulk import employees from a CSV file with validation
- Ensure date formats are correct (YYYY-MM-DD) during import/export

---

## ⚙️ How to Run

1. Clone the repository
   
cd <your-project-folder>
git clone https://github.com/mhardyn/final_project.git

2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install dependencies

pip install Django

4. Run database migrations

python manage.py makemigrations
python manage.py migrate

5. (Optional) Import employees from CSV

python manage.py import_employees

6. Start the development server

python manage.py runserver

7. Open your browser and visit:

http://localhost:8000/

### 🚨 Important Notes

The PESEL number is used as a unique identifier and username in the system.
Date fields (like date of employment) must be in YYYY-MM-DD format.
The system enforces a limit of 5 employees on holiday per day to ensure adequate staffing.
Each employee is allowed up to 26 holiday days per calendar year.
When employees are added or removed, both the Django model and the CSV file (if used) must be kept synchronized manually or via custom scripts.
Default passwords for new users are set to 'defaultpassword' — be sure to change this for production.

### 📂 Project Structure

employee_management_system/ — main Django app with models, views, and templates
management/commands/import_employees.py — custom command to import employees from CSV
templates/employee_management_system/ — HTML templates for UI
static/ — static assets (CSS, JS)

### 🛠️ Technologies

Python 3.12+
Django 4.x
SQLite / PostgreSQL (configurable)
HTML, CSS (Bootstrap optional)
