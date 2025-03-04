from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth.views import LogoutView

# Patient Model
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ])

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date_time}"

# Inventory Model
class Inventory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField()

    def __str__(self):
        return self.name

# Transaction Model
class Transaction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.patient} - {self.date} - {self.amount}"

# Delete Patient View
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.delete()
        return redirect('patient_list')
    return redirect('patient_list')

# Custom Logout View (Optional)
def custom_logout(request):
    logout(request)
    return redirect('/')

# URL Patterns
urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),  # Recommended
    # path("logout/", custom_logout, name="logout"),  # Alternative if you want GET logout
]
