from django import forms
from django.forms import ModelForm, TextInput, DateInput
from .models import Staff_data

class UserInfoForm(ModelForm):
    class Meta:
        model = Staff_data
        # fields = ['staff_id', 'firstname', 'lastname', 'dob', 'email', 'phone_number', 'position']
        fields = ['staff_id']
        widgets = {
            'staff_id' : TextInput(attrs ={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder':'Staff id',
            }),
            # 'firstname': ,
            # 'lastname': ,
            # 'dob': ,
            # 'email':
            # 'phone_number': ,
            # 'position': ,
        }