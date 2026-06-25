from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    
    # Auth
    path('signup/patient/', views.signup_patient, name='signup_patient'),
    path('signup/doctor/', views.signup_doctor, name='signup_doctor'),
    path('check_username/', views.check_username, name='check_username'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Dashboards
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/doctor/history/', views.doctor_history, name='doctor_history'),
    path('dashboard/doctor/action/<int:appt_id>/<str:status>/', views.doctor_appointment_action, name='doctor_action'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/appointments/', views.admin_appointments, name='admin_appointments'),
    path('dashboard/admin/doctors/', views.admin_doctors, name='admin_doctors'),
    path('dashboard/admin/doctors/add/', views.admin_add_doctor, name='admin_add_doctor'),
    path('dashboard/admin/doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('dashboard/admin/patients/', views.admin_patients, name='admin_patients'),
    path('dashboard/admin/patients/add/', views.admin_add_patient, name='admin_add_patient'),
    path('dashboard/admin/patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('dashboard/admin/departments/', views.admin_departments, name='admin_departments'),
    path('dashboard/admin/departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('dashboard/admin/diseases/', views.admin_diseases, name='admin_diseases'),
    path('dashboard/admin/diseases/delete/<int:disease_id>/', views.delete_disease, name='delete_disease'),
    path('dashboard/admin/admins/', views.admin_manage_admins, name='admin_manage_admins'),
    
    # AI Specialist (Symptom Checker)
    path('find-specialist/', views.find_specialist, name='find_specialist'),
    
    # Appointment
    path('book/<int:department_id>/', views.book_appointment, name='book_appointment'),
    path('appointment-history/', views.appointment_history, name='appointment_history'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appointment/update/<int:appt_id>/<str:status>/', views.update_appointment_status, name='update_status'),
]
