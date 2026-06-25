import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')
django.setup()

from django.contrib.auth.models import User
from recommendation.models import Profile, Doctor, Department

def seed_users():
    # 1. Create Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.profile.role = 'admin'
        admin.profile.save()
        print("Admin created: admin / admin123")

    # 2. Create a Doctor User
    if not User.objects.filter(username='doctor1').exists():
        doc_user = User.objects.create_user('doctor1', 'doc@example.com', 'pass123')
        doc_user.profile.role = 'doctor'
        doc_user.profile.save()
        
        # Link to a Doctor model
        dept = Department.objects.first()
        if dept:
            Doctor.objects.create(
                user=doc_user,
                name="Stephen Strange",
                department=dept,
                specialization="Master of Arts",
                availability="Anytime"
            )
        print("Doctor created: doctor1 / pass123")

    # 3. Create a Patient User
    if not User.objects.filter(username='patient1').exists():
        pat_user = User.objects.create_user('patient1', 'pat@example.com', 'pass123')
        pat_user.profile.role = 'patient'
        pat_user.profile.save()
        print("Patient created: patient1 / pass123")

if __name__ == '__main__':
    seed_users()
