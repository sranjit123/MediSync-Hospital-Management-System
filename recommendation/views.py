from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Department, Doctor, Disease, Appointment, Patient, Admin
from .ai.algorithm import recommend_department

# --- Auth Views ---

from django.http import JsonResponse

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': CustomUser.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def signup_patient(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")

        if CustomUser.objects.filter(username=u).exists():
            return render(request, "recommendation/shared/signup_patient.html", {"error": "Username already exists"})
        
        # Validation
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", e):
            return render(request, "recommendation/shared/signup_patient.html", {"error": "Invalid email address"})
        
        if len(p) < 8:
            return render(request, "recommendation/shared/signup_patient.html", {"error": "Password must be at least 8 characters"})

        patient = Patient.objects.create_user(
            username=u, password=p, email=e, 
            full_name=full_name, image=image, role='patient'
        )
        login(request, patient)
        return redirect('patient_dashboard')
    
    return render(request, "recommendation/shared/signup_patient.html")

def signup_doctor(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")
        full_name = request.POST.get("full_name")
        dept_id = request.POST.get("department")
        spec = request.POST.get("specialization")
        avail = request.POST.get("availability")
        image = request.FILES.get("image")

        if CustomUser.objects.filter(username=u).exists():
            return render(request, "recommendation/shared/signup_doctor.html", {
                "error": "Username already exists",
                "departments": Department.objects.all()
            })
        
        dept = get_object_or_404(Department, id=dept_id)
        doctor = Doctor.objects.create_user(
            username=u, password=p, email=e, 
            full_name=full_name, department=dept, 
            specialization=spec, availability=avail, 
            image=image, role='doctor'
        )
        login(request, doctor)
        return redirect('doctor_dashboard')
    
    departments = Department.objects.all()
    return render(request, "recommendation/shared/signup_doctor.html", {"departments": departments})

def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        role_selected = request.POST.get("role")
        
        user = authenticate(username=u, password=p)
        if user:
            if user.role == role_selected:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('patient_dashboard')
            else:
                return render(request, "recommendation/shared/login.html", {"error_msg": f"Account exists but not as a {role_selected}"})
        else:
            return render(request, "recommendation/shared/login.html", {"error_msg": "Invalid credentials"})
    return render(request, "recommendation/shared/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    if request.method == "POST":
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        image = request.FILES.get('image')
        
        user = request.user
        user.email = email
        user.full_name = full_name
        if image:
            user.image = image
        user.save()
        return redirect('user_profile')
        
    return render(request, "recommendation/shared/profile.html")

# --- Role Dashboards ---

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('login')
    
    # Cast to Patient model for easier access
    patient = get_object_or_404(Patient, id=request.user.id)
    query = request.GET.get('q', '').strip()
    departments = Department.objects.prefetch_related('doctors_list').all()
    
    dept_doctors = []
    for dept in departments:
        doctors = dept.doctors_list.all()
        if query:
            doctors = doctors.filter(full_name__icontains=query) | doctors.filter(specialization__icontains=query)
        
        if doctors.exists() or not query:
            dept_doctors.append({
                'id': dept.id,
                'name': dept.name,
                'doctors': doctors
            })
        
    return render(request, "recommendation/patient/dashboard_patient.html", {
        "dept_doctors": dept_doctors,
        "query": query,
        "patient": patient
    })

@login_required
def appointment_history(request):
    if request.user.role != 'patient':
        return redirect('login')
    patient = get_object_or_404(Patient, id=request.user.id)
    appointments = patient.appointments.all().order_by('-created_at')
    return render(request, "recommendation/patient/appointment_history.html", {
        "appointments": appointments
    })

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('login')
    
    doctor = get_object_or_404(Doctor, id=request.user.id)
    appointments = doctor.appointments.all().order_by('appointment_date', 'appointment_time')
    
    stats = {
        "treated_count": appointments.filter(status='completed').count(),
        "accepted_count": appointments.filter(status='accepted').count(),
        "pending_count": appointments.filter(status='pending').count(),
        "rejected_count": appointments.filter(status='rejected').count(),
    }
    
    upcoming = appointments.filter(status='accepted').order_by('appointment_date', 'appointment_time')[:5]
        
    return render(request, "recommendation/doctor/dashboard_doctor.html", {
        "upcoming": upcoming,
        **stats,
        "doctor": doctor
    })

@login_required
def doctor_history(request):
    if request.user.role != 'doctor':
        return redirect('login')
    
    doctor = get_object_or_404(Doctor, id=request.user.id)
    query = request.GET.get('q', '')
    appointments = doctor.appointments.all().order_by('-appointment_date')
    
    if query:
        appointments = appointments.filter(patient__full_name__icontains=query) | \
                       appointments.filter(symptoms__icontains=query)
                       
    return render(request, "recommendation/doctor/doctor_history.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def doctor_appointment_action(request, appt_id, status):
    if request.user.role != 'doctor':
        return redirect('login')
    
    doctor = get_object_or_404(Doctor, id=request.user.id)
    appointment = get_object_or_404(Appointment, id=appt_id, doctor=doctor)
    if status in ['accepted', 'rejected', 'completed']:
        appointment.status = status
        appointment.save()
    return redirect('doctor_dashboard')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    context = {
        "doctor_count": Doctor.objects.count(),
        "patient_count": Patient.objects.count(),
        "department_count": Department.objects.count(),
        "pending_count": Appointment.objects.filter(status='pending').count(),
    }
    return render(request, "recommendation/admin/dashboard_admin.html", context)

@login_required
def admin_appointments(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    query = request.GET.get('q', '')
    appointments = Appointment.objects.all().order_by('-created_at')
    
    if query:
        appointments = appointments.filter(patient__full_name__icontains=query) | \
                       appointments.filter(doctor__full_name__icontains=query)
                       
    return render(request, "recommendation/admin/admin_appointments.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def admin_doctors(request):
    if request.user.role != 'admin':
        return redirect('login')
    doctors = Doctor.objects.all()
    return render(request, "recommendation/admin/admin_doctors.html", {"doctors": doctors})

@login_required
def admin_patients(request):
    if request.user.role != 'admin':
        return redirect('login')
    patients = Patient.objects.all()
    return render(request, "recommendation/admin/admin_patients.html", {"patients": patients})

@login_required
def admin_add_doctor(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")
        full_name = request.POST.get("full_name")
        dept_id = request.POST.get("department")
        spec = request.POST.get("specialization")
        avail = request.POST.get("availability")
        image = request.FILES.get("image")
        
        if CustomUser.objects.filter(username=u).exists():
            return render(request, "recommendation/admin/admin_add_doctor.html", {
                "error": "Username already exists",
                "departments": Department.objects.all()
            })
            
        dept = get_object_or_404(Department, id=dept_id)
        Doctor.objects.create_user(
            username=u, password=p, email=e, 
            full_name=full_name, department=dept, 
            specialization=spec, availability=avail, 
            image=image, role='doctor'
        )
        return redirect('admin_doctors')
        
    departments = Department.objects.all()
    return render(request, "recommendation/admin/admin_add_doctor.html", {"departments": departments})

@login_required
def admin_add_patient(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        
        if CustomUser.objects.filter(username=u).exists():
            return render(request, "recommendation/admin/admin_add_patient.html", {"error": "Username already exists"})
            
        Patient.objects.create_user(
            username=u, password=p, email=e, 
            full_name=full_name, image=image, role='patient'
        )
        return redirect('admin_patients')
        
    return render(request, "recommendation/admin/admin_add_patient.html")

@login_required
def admin_manage_admins(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")
        full_name = request.POST.get("full_name")
        
        if CustomUser.objects.filter(username=u).exists():
            admins = Admin.objects.all()
            return render(request, "recommendation/admin/admin_manage_admins.html", {
                "error": "Username already exists",
                "admins": admins
            })
            
        Admin.objects.create_user(
            username=u, password=p, email=e, 
            full_name=full_name, role='admin'
        )
        return redirect('admin_manage_admins')
        
    admins = Admin.objects.all()
    return render(request, "recommendation/admin/admin_manage_admins.html", {"admins": admins})

@login_required
def delete_doctor(request, doctor_id):
    if request.user.role != 'admin':
        return redirect('login')
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('admin_doctors')

@login_required
def delete_patient(request, patient_id):
    if request.user.role != 'admin':
        return redirect('login')
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('admin_patients')

@login_required
def admin_departments(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        keywords = request.POST.get("keywords")
        Department.objects.create(name=name, description=description, keywords=keywords)
        return redirect('admin_departments')
        
    departments = Department.objects.all()
    return render(request, "recommendation/admin/admin_departments.html", {"departments": departments})

@login_required
def delete_department(request, dept_id):
    if request.user.role != 'admin':
        return redirect('login')
    dept = get_object_or_404(Department, id=dept_id)
    dept.delete()
    return redirect('admin_departments')

@login_required
def admin_diseases(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == "POST":
        name = request.POST.get("name")
        department_id = request.POST.get("department")
        symptoms = request.POST.get("symptoms")
        dept = get_object_or_404(Department, id=department_id)
        Disease.objects.create(name=name, department=dept, symptoms=symptoms)
        
        # Sync keywords
        new_keywords = set(dept.keywords.split())
        for symptom in symptoms.split(','):
            for word in symptom.split():
                clean_word = word.strip().lower()
                if clean_word:
                    new_keywords.add(clean_word)
        dept.keywords = ' '.join(list(new_keywords))
        dept.save()

        return redirect('admin_diseases')
        
    diseases = Disease.objects.all().order_by('department__name')
    departments = Department.objects.all()
    return render(request, "recommendation/admin/admin_diseases.html", {"diseases": diseases, "departments": departments})

@login_required
def delete_disease(request, disease_id):
    if request.user.role != 'admin':
        return redirect('login')
    disease = get_object_or_404(Disease, id=disease_id)
    disease.delete()
    return redirect('admin_diseases')

@login_required
def update_appointment_status(request, appt_id, status):
    if request.user.role != 'admin':
        return redirect('login')
    
    appointment = get_object_or_404(Appointment, id=appt_id)
    if status in ['accepted', 'rejected']:
        appointment.status = status
        appointment.save()
    return redirect('admin_dashboard')

# --- Main Pages ---

def landing(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    stats = {
        "doctor_count": Doctor.objects.count(),
        "department_count": Department.objects.count(),
        "patient_count": Patient.objects.count(),
        "successful_matches": 1250,
    }
    return render(request, "recommendation/public/landing.html", {
        "departments": departments,
        "doctors": doctors,
        "stats": stats
    })

def home(request):
    if request.user.is_authenticated:
        role = request.user.role
        if role == 'admin': return redirect('admin_dashboard')
        if role == 'doctor': return redirect('doctor_dashboard')
        return redirect('patient_dashboard')
    return redirect('landing')

# --- AI Specialist Logic ---

def find_specialist(request):
    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").lower().strip()
        department = recommend_department(symptoms)

        if department:
            doctors = department.doctors_list.all()
            related_diseases = department.diseases.all()
            return render(request, "recommendation/ai/result.html", {
                "department": department,
                "doctors": doctors,
                "related_diseases": related_diseases,
                "symptoms": symptoms
            })
        else:
            return render(request, "recommendation/ai/result.html", {
                "error": True,
                "symptoms": symptoms
            })
            
    return render(request, "recommendation/ai/find_specialist.html")

def is_doctor_available(doctor, date_str, time_str):
    """
    Simple parser for doctor availability.
    Expected format in DB: 'Mon-Fri 09:00-17:00' or similar
    """
    import datetime
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        appt_time = datetime.datetime.strptime(time_str, '%H:%M').time()
        day_of_week = dt.strftime('%a') # Mon, Tue, etc.
        
        raw_avail = doctor.availability.lower()
        
        # Super simple check: if 'mon-fri' is in string and it's a weekday
        is_weekday = day_of_week in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        if 'mon-fri' in raw_avail and is_weekday:
            # Check time range (find 09:00-17:00 in string)
            import re
            match = re.search(r'(\d{2}:\d{2})-(\d{2}:\d{2})', raw_avail)
            if match:
                start = datetime.datetime.strptime(match.group(1), '%H:%M').time()
                end = datetime.datetime.strptime(match.group(2), '%H:%M').time()
                return start <= appt_time <= end
        
        # If no specific pattern found, just allow it but log (for demo flexibility)
        # In a real app, we'd be much stricter.
        return True
    except Exception as e:
        print(f"Availability check error: {e}")
        return True

@login_required
def book_appointment(request, department_id):
    if request.user.role != 'patient':
        return redirect('patient_dashboard')

    department = get_object_or_404(Department, id=department_id)
    doctors = department.doctors_list.all()
    patient = get_object_or_404(Patient, id=request.user.id)
    
    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time")
        symptoms = request.POST.get("symptoms", "")
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        if not is_doctor_available(doctor, date, time):
            return render(request, "recommendation/patient/book_appointment.html", {
                "department": department,
                "doctors": doctors,
                "error": f"Dr. {doctor.full_name} is not available on {date} at {time}. Please check their availability: {doctor.availability}"
            })
        
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            symptoms=symptoms
        )
        
        return render(request, "recommendation/patient/appointment_success.html", {"appointment": appointment})
        
    return render(request, "recommendation/patient/book_appointment.html", {
        "department": department,
        "doctors": doctors
    })

def appointment_success(request):
    return render(request, "recommendation/patient/appointment_success.html")
