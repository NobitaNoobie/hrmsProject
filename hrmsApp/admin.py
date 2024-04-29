# this is optional, but you can register your models here 
from django.contrib import admin
from .models import LeaveApplication

# Register your models here.
admin.site.register(LeaveApplication)