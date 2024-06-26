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
    path("leave_frequency/<str:employee_id>/", views.leave_frequency, name='leave_frequency'),
    path("leave_rejection_rate/<str:employee_id>/", view=views.leave_rejection_rate, name='leave_rejection_rate'),
    path("absenteeism_rate/", views.absenteeism_rate, name="absenteeism_rate"),
    path("absenteeism_rate_monthly/<int:month_val>/<int:year_val>/", views.absenteeism_rate_monthly ,name="absenteeism_rate_monthly"),
    path("absenteeism_rate_list/<int:year>/", view= views.absenteeism_rate_list, name='absenteeism_rate_list'),
    path("num_absentees_future/", views.num_absentees_future, name="num_absentees_future"),
    path("regform/", views.regform, name="regform"),
    path("planned_leaves/", views.planned_leaves, name="planned_leaves"),
    path("unplanned_leaves/", views.unplanned_leaves, name="unplanned_leaves"),
    path("num_employees_on_leave_monthly/", views.num_employees_on_leave_monthly, name="num_employees_on_leave_monthly"),
    path("absenteeism_rate_relative/<int:month_val>/<int:year_val>/", views.absenteeism_rate_relative, name='absenteeism_rate_relative'),
]