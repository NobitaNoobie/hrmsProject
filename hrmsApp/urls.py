from django.urls import path
from . import views

urlpatterns = [
    path("employeeList/", views.employee_list, name="employee list"),
    #path("employeeHome/", views.employeehome, name='employee_home'),
    path("employeeHome/<str:employee_id>/", views.employeehome, name="employee_home"),
    path("leaveApply/<str:employee_id>", views.applyLeave, name="leave application dashboard"),
    path("leave_applications_on_date/<str:date>/", views.leave_applications_on_date, name="leave_applications_on_date"),
    path("leave_applications_on_today/", views.leave_applications_on_today, name="leave_applications_on_today"),
    path("num_employees_on_leave_today/", views.num_employees_on_leave_today, name='num_employees_on_leave_today'),
    path("num_employees_on_leave_on_day/<str:date>/", views.num_employees_on_leave_on_day, name="num_employees_on_leave_on_day"),
    path("wfh_frequency/<str:employee_id>/", views.wfh_frequency, name='wfh_frequency'),
    path("leave_frequency/<str:employee_id>/", views.leave_frequency, name='leave_frequency')
]