from django.urls import path
from . import views

urlpatterns = [
    path('holidays/view/', views.holidays_view, name='holidays_view_url'),
    path('holidays/add/', views.add_holiday, name='add_holiday_url'),
    path('holidays/events_json/', views.holidays_events_json, name='holidays_events_json_url'),
    path('holidays/delete/', views.delete_holiday, name='delete_holiday_url'),
    path('holidays/remaining_days/', views.get_remaining_days, name='remaining_days_url'),
    path('employee/search/', views.employee_search, name='employee_search_url'),
    path('employee/delete/<str:pesel>/', views.delete_employee, name='delete_employee_url'),
    path('employee/add/', views.add_employee, name='add_employee_url'),
    path('statistics/', views.statistics, name='statistics_url'),
    path('employee/<str:pesel>/edit/', views.employee_edit, name='employee_edit_url'),
    path('<str:pesel>/', views.employee_detail, name='employee_detail_url'),
    path('', views.all_employees, name='all_employees_url'),
]

