import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')
django.setup()

from recommendation.models import Department, Admin, CustomUser

def seed():
    # 1. Create Departments
    depts = [
        ("Cardiology", "Heart and circulatory system specialist", "heart, chest pain, pulse, blood pressure"),
        ("Neurology", "Brain and nervous system specialist", "headache, dizziness, seizure, numbness"),
        ("Orthopedics", "Bones and muscles specialist", "fractures, joint pain, back pain, sports injury"),
        ("Pediatrics", "Medical care for children", "fever, cough, child growth, vaccination"),
        ("Dermatology", "Skin, hair, and nail specialist", "rash, acne, skin allergy, itching"),
    ]

    for name, desc, keywords in depts:
        dept, created = Department.objects.get_or_create(name=name, defaults={'description': desc, 'keywords': keywords})
        if created:
            print(f"Created department: {name}")

    # 2. Create Admin
    if not Admin.objects.filter(username="admin").exists():
        Admin.objects.create_user(
            username="admin", 
            password="adminpassword123", 
            email="admin@hospital.com",
            full_name="Hospital Administrator",
            role="admin"
        )
        print("Created admin user: admin / adminpassword123")

if __name__ == "__main__":
    seed()
