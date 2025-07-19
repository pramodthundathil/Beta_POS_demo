from django.db import models
import random
from django.contrib.auth.models import User

class Staff(models.Model):
    employe_id = models.CharField(unique=True, max_length=20)
    employee_name = models.CharField(max_length=20)
    designation = models.CharField(max_length=20, choices=(("Sales Man","Sales Man"),("Manager","Manager"),("Other","Other")))
    date_of_join = models.DateField(auto_now_add=False, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.employe_id:
            self.employe_id = self.generate_eid_number()
        super().save(*args, **kwargs)

    def generate_eid_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(100, 999)  # 5-digit random number
            order_number = f"{random_number}"
            if not Staff.objects.filter(employe_id=order_number).exists():
                return order_number
            
    def __str__(self):
        return str(self.employee_name + f" (Emp Id:{self.employe_id})")


class StaffSalary(models.Model):
    slip_no = models.CharField(max_length=20)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    amount = models.FloatField()
    month = models.CharField(max_length=20)
    date_of_salary = models.DateField()
    date = models.DateField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.slip_no:
            self.slip_no = self.generate_slip_number()
        super().save(*args, **kwargs)

    def generate_slip_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(10000, 999999)  # 5-digit random number
            order_number = f"SALARY-{random_number}"
            if not StaffSalary.objects.filter(slip_no=order_number).exists():
                return order_number
            

class Notification(models.Model):
    notification_heading = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ref_number = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.notification_heading}"
    

class Profile(models.Model):
    Profile_name = models.CharField(max_length=255)
    logo = models.FileField(upload_to='Logo')
    user = models.ManyToManyField(User)
