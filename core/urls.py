from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('edit-patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:id>/', views.delete_patient, name='delete_patient'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
]