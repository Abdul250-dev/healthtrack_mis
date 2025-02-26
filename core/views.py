from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Patient, Doctor, Appointment, Inventory, Transaction
from django.db import models

@never_cache
@login_required
def dashboard(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'low_stock_items': Inventory.objects.filter(quantity__lte=models.F('reorder_level')),
    }
    return render(request, 'core/dashboard.html', context)

@never_cache
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'core/patient_list.html', {'patients': patients})

@never_cache
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'core/appointment_list.html', {'appointments': appointments})

@never_cache
@login_required
def inventory_list(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'core/inventory_list.html', {'inventory_items': inventory_items})

@never_cache
@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'core/transaction_list.html', {'transactions': transactions})

@never_cache
@login_required
def register_patient(request):
    if request.method == "POST":
        # Collecting patient-specific data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['dob']
        phone_number = request.POST['phone']
        address = request.POST['address']
        gender = request.POST['gender']
        blood_type = request.POST.get('blood_type', '')
        emergency_contact = request.POST.get('emergency_contact', '')

        # Create Patient object with the additional fields
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            address=address,
            gender=gender,
            blood_type=blood_type,
            emergency_contact=emergency_contact
        )

        messages.success(request, 'Patient registered successfully.')
        return redirect('patient_list')  # Redirect to patient list after registration

    return render(request, "core/register_patient.html")

@never_cache
@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        # Update patient data
        patient.first_name = request.POST['first_name']
        patient.last_name = request.POST['last_name']
        patient.date_of_birth = request.POST['dob']
        patient.phone_number = request.POST['phone']
        patient.address = request.POST['address']
        patient.gender = request.POST['gender']
        patient.blood_type = request.POST.get('blood_type', '')
        patient.emergency_contact = request.POST.get('emergency_contact', '')
        patient.save()
        return redirect('patient_list')
    return render(request, 'core/edit_patient.html', {'patient': patient})

@never_cache
@login_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
    return redirect('patient_list')