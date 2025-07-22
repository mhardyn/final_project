from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Employee, Holiday

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'pesel', 'email', 'salary')
    search_fields = ('name', 'surname', 'pesel', 'email')
    list_filter = ('date_of_employment',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date')
    list_filter = ('date',)
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name')


