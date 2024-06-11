from django.db import models
import re
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_emp_code(value):
    if not re.match(r'^GSTN[TC]\d+$', value):
        raise ValidationError('Employee code must start with GSTNT or GSTNC and be followed by digits.')

class Employee_data(models.Model):
    NEW_LEVEL_CHOICES = [
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
        ('L4', 'L4'),
        ('L5', 'L5'),
    ]

    NEW_GRADE_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3a', '3a'),
        ('3b', '3b'),
        ('4a', '4a'),
        ('4b', '4b'),
        ('4c', '4c'),
        ('5a', '5a'),
        ('5b', '5b'),
        ('5c', '5c'),
    ]

    DESIGNATION_CHOICES = [
        ('CEO', 'CEO'),
        ('CTO', 'CTO'),
        ('EVP', 'EVP'),
        ('SVP', 'SVP'),
        ('VP', 'VP'),
        ('AVP / Chief Engineer', 'AVP / Chief Engineer'),
        ('Assoc. VP / Principal Engineer', 'Assoc. VP / Principal Engineer'),
        ('SM / Tech Lead', 'SM / Tech Lead'),
        ('Manager / Sr Engineer', 'Manager / Sr Engineer'),
        ('AM / Engineer', 'AM / Engineer'),
        ('Executive / Assoc. Engineer', 'Executive / Assoc. Engineer'),
    ]

    VERTICAL_CHOICES = [
        ('Technology', 'Technology'),
        ('Services', 'Services'),
        ('Support', 'Support'),
        ('Others', 'Others'),
    ]

    EMPLOYEE_TYPE_CHOICES = [
        ('Consultant', 'Consultant'),
        ('Market Hire', 'Market Hire'),
        ('Deputation', 'Deputation'),
    ]

    CURRENT_STATUS_CHOICES = [
        ('Working', 'Working'),
        ('Exit', 'Exit'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
    ]

    s_no = models.AutoField(primary_key=True)
    emp_code = models.CharField(max_length=50, validators=[validate_emp_code], unique=True)
    full_name = models.CharField(max_length=100)
    total_experience = models.CharField(max_length=50)
    new_level = models.CharField(max_length=2, choices=NEW_LEVEL_CHOICES)
    new_grade = models.CharField(max_length=3, choices=NEW_GRADE_CHOICES)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    vertical = models.CharField(max_length=100, choices=VERTICAL_CHOICES)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    reporting_manager = models.CharField(max_length=100)
    review_manager = models.CharField(max_length=100)
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    doj = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    mobile_number = models.CharField(max_length=10)
    official_mail_id = models.EmailField(max_length=100)
    personal_mail_id = models.EmailField(max_length=100)
    father_name = models.CharField(max_length=100)
    address = models.TextField()
    dob = models.DateField()
    #model instance reference
    dob_month = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=10)
    contact_person_for_emergency = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    relation_with_employee = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    aniv_date = models.DateField()
    aniv_month = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    last_working_day = models.DateField()
    employee_type = models.CharField(max_length=50, choices=EMPLOYEE_TYPE_CHOICES)
    current_status = models.CharField(max_length=50, choices=CURRENT_STATUS_CHOICES)
    exit_year = models.IntegerField()
    pan_no = models.CharField(max_length=10)
    aadhaar_no = models.CharField(max_length=16)
    qualification_degree = models.CharField(max_length=100)
    qualification_master = models.CharField(max_length=100)
    remark = models.TextField()
    insurance_family_details = models.JSONField()

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        monthdob = datetime.strptime(self.dob , '%B')
        self.dob_month = monthdob.strftime('%B')
        super(Employee_data, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'employee_data'
