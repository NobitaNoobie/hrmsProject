from django.db import models
#inherit from the models class to tell django that this is where we have our models

from django.utils import timezone

# Create your models here.
# below is where the inheritance from models class takes place

class Emp_Leave_Data(models.Model):
    auto_id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=255) 
    leave_type = models.CharField(max_length=255) 
    leave_description = models.CharField(max_length= 5000)
    leave_from = models.DateField()
    leave_to = models.DateField()
    leave_days = models.DecimalField(max_digits=7, decimal_places=2)
    date_of_request =  models.DateTimeField(default=timezone.now)
    approval_status = models.CharField(max_length=255)

    class Meta:
        db_table = 'emp_leave_data'

class LeaveApplication(models.Model):
    employee_id = models.CharField(primary_key=True, max_length=8, verbose_name="employee_id")
    employee_name = models.CharField(max_length=50)

    RESTRICTED_HOLIDAY = "RH"
    CASUAL_LEAVE = "CL"
    EARNED_LEAVE = "EL"
    WORK_FROM_HOME = "WFH"

    LEAVE_TYPES_CHOICES = {
        RESTRICTED_HOLIDAY: "Restricted Holiday",
        CASUAL_LEAVE: "Casual Leave",
        EARNED_LEAVE: "Earned leave",
        WORK_FROM_HOME: "Work from home",
    }
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES_CHOICES, default=CASUAL_LEAVE)
    #app_leave = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    app_leave_cl = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    app_leave_el = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    app_leave_rh = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    #available_leave_balance = models.DecimalField(max_digits=4, decimal_places=2, default=30.00)
    #float field does not allow specifying the decimal places
    
    available_leave_balance_cl = models.DecimalField(max_digits=4, decimal_places=2, default=8.00)
    available_leave_balance_rh = models.DecimalField(max_digits=4, decimal_places=2, default=2.00)
    available_leave_balance_el = models.DecimalField(max_digits=4, decimal_places=2, default=30.00)

    has_applied = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.employee_name + ' ' + self.employee_id

    class Meta:
        db_table = 'hrms_leaveapplication'
    
