import os
import re

filepath = r"e:\College\Semester\project2\recommendation\views.py"
with open(filepath, 'r') as f:
    content = f.read()

replacements = {
    'recommendation/admin_add_doctor.html': 'recommendation/admin/admin_add_doctor.html',
    'recommendation/admin_add_patient.html': 'recommendation/admin/admin_add_patient.html',
    'recommendation/admin_appointments.html': 'recommendation/admin/admin_appointments.html',
    'recommendation/admin_departments.html': 'recommendation/admin/admin_departments.html',
    'recommendation/admin_doctors.html': 'recommendation/admin/admin_doctors.html',
    'recommendation/admin_manage_admins.html': 'recommendation/admin/admin_manage_admins.html',
    'recommendation/admin_patients.html': 'recommendation/admin/admin_patients.html',
    'recommendation/appointment_history.html': 'recommendation/patient/appointment_history.html',
    'recommendation/appointment_success.html': 'recommendation/patient/appointment_success.html',
    'recommendation/book_appointment.html': 'recommendation/patient/book_appointment.html',
    'recommendation/dashboard_admin.html': 'recommendation/admin/dashboard_admin.html',
    'recommendation/dashboard_doctor.html': 'recommendation/doctor/dashboard_doctor.html',
    'recommendation/dashboard_patient.html': 'recommendation/patient/dashboard_patient.html',
    'recommendation/doctor_history.html': 'recommendation/doctor/doctor_history.html',
    'recommendation/home.html': 'recommendation/public/home.html',
    'recommendation/home_template.html': 'recommendation/public/home_template.html',
    'recommendation/landing.html': 'recommendation/public/landing.html',
    'recommendation/login.html': 'recommendation/shared/login.html',
    'recommendation/result.html': 'recommendation/public/result.html',
    'recommendation/signup.html': 'recommendation/shared/signup.html'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(filepath, 'w') as f:
    f.write(content)

print("Views updated.")
