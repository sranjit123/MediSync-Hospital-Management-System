from django.contrib import admin
from .models import Department, Doctor, Disease, Appointment, CustomUser, Admin, Patient

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'role')
    list_filter = ('role',)

@admin.register(Admin)
class AdminModel(admin.ModelAdmin):
    list_display = ('username', 'full_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'keywords')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'specialization', 'availability')
    list_filter = ('department', 'specialization')
    search_fields = ('full_name',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username')

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'symptoms')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__full_name', 'symptoms')
