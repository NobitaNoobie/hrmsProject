from django.urls import path
from . import views

urlpatterns = [
    path("employeeList/", views.employee_list, name="employee list"),
    #path("employeeHome/", views.employeehome, name='employee_home'),
    path("employeeHome/<str:employee_id>", views.employeehome, name="employee_home"),
    path("leaveApply/<str:employee_id>", views.applyLeave, name="leave application dashboard")
]