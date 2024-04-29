#the process of going from a python object to json is described here.
from rest_framework import serializers

from hrmsApp.models import LeaveApplication
class HrmsAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['employee_id', 'employee_name', 'leave_type', 'app_leave_rh', 'app_leave_cl', 'app_leave_el', 'available_leave_balance_rh', 'available_leave_balance_el', 'available_leave_balance_cl', 'has_applied', 'is_verified', 'start_date', 'end_date']