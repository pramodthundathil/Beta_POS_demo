from django import forms
from .models import Staff
from .models import StaffSalary


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [ 'employee_name', 'designation', 'date_of_join', 'address']
        widgets = {
            # 'emplaye_id': forms.TextInput(attrs={'id': 'emplaye_id', 'class': 'form-control'}),
            'employee_name': forms.TextInput(attrs={'id': 'employee_name', 'class': 'form-control'}),
            'designation': forms.Select(attrs={'id': 'designation', 'class': 'form-control'}),
            'date_of_join': forms.DateInput(attrs={'id': 'date_of_join', 'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'id': 'address', 'class': 'form-control', 'rows': 4}),
        }



class StaffSalaryForm(forms.ModelForm):
    class Meta:
        model = StaffSalary
        fields = ['staff', 'amount', 'month', 'date_of_salary']
        widgets = {
            'staff': forms.Select(attrs={'id': 'staff', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'id': 'amount', 'class': 'form-control'}),
            'month': forms.TextInput(attrs={'id': 'month', 'class': 'form-control'}),
            'date_of_salary': forms.DateInput(attrs={'id': 'date_of_salary', 'class': 'form-control', 'type': 'date'}),
        }
