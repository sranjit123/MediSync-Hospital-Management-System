from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"

class Admin(CustomUser):
    class Meta:
        db_table = 'admin'
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    keywords = models.TextField(help_text="Comma-separated symptoms or keywords related to this department")

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name

class Doctor(CustomUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors_list')
    specialization = models.CharField(max_length=200)
    availability = models.TextField(help_text="Format: Day StartTime-EndTime (e.g. Mon 09:00-17:00)", default="Mon-Fri 09:00-17:00")

    class Meta:
        db_table = 'doctor'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.full_name} ({self.department.name})"

class Patient(CustomUser):
    class Meta:
        db_table = 'patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"{self.full_name} (Patient)"

class Disease(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='diseases')
    symptoms = models.TextField(help_text="Comma-separated symptoms")

    class Meta:
        db_table = 'disease'

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return f"Appointment: {self.patient.full_name} with {self.doctor.full_name} ({self.status})"
