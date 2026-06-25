import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')
django.setup()

from recommendation.models import Department, Doctor, Disease

def seed():
    # Clear existing data
    Department.objects.all().delete()
    print("Cleared existing data.")

    # Department 1: Cardiology
    cardio = Department.objects.create(
        name="Cardiology",
        description="Deals with disorders of the heart and the cardiovascular system.",
        keywords="heart chest pain pulse blood pressure palpitations shortness of breath angina arm pain jaw pain sweating rapid heartbeat irregular beat fainting hypertension cholesterol syncope"
    )
    Doctor.objects.create(name="Strange", department=cardio, specialization="Cardiologist", availability="Mon-Fri, 9AM-5PM")
    Doctor.objects.create(name="House", department=cardio, specialization="Cardiac Surgeon", availability="Tue-Thu, 10AM-4PM")
    Disease.objects.create(name="Coronary Artery Disease", department=cardio, symptoms="chest pain, shortness of breath, fatigue")
    Disease.objects.create(name="Heart Attack", department=cardio, symptoms="crushing chest pain, radiation to left arm, sweating, nausea, shortness of breath")
    Disease.objects.create(name="Arrhythmia", department=cardio, symptoms="palpitations, irregular heartbeat, dizzy spells")

    # Department 2: Neurology
    neuro = Department.objects.create(
        name="Neurology",
        description="Deals with disorders of the nervous system.",
        keywords="headache brain dizziness dizzy seizing seizure vision balance memory loss numbness stroke tingling weakness tremor fainting paralysis confusion slurred speech coordination back nerve spine"
    )
    Doctor.objects.create(name="Shepherd", department=neuro, specialization="Neurologist", availability="Mon-Wed, 8AM-2PM")
    Doctor.objects.create(name="Lecter", department=neuro, specialization="Neurosurgeon", availability="Thu-Sat, 9AM-3PM")
    Disease.objects.create(name="Migraine", department=neuro, symptoms="intense throbbing headache, nausea, sensitivity to light, aura")
    Disease.objects.create(name="Stroke", department=neuro, symptoms="sudden weakness on one side, confusion, trouble speaking, facial drooping")
    Disease.objects.create(name="Epilepsy", department=neuro, symptoms="recurrent seizures, temporary confusion")

    # Department 3: Orthopedics
    ortho = Department.objects.create(
        name="Orthopedics",
        description="Focuses on injuries and diseases of your body's musculoskeletal system.",
        keywords="bone joint pain fracture muscle skeleton back pain knee pain shoulder pain spine hip ankle wrist swelling stiffness arthritis sprain ligament tendon slipped disc mobility cast"
    )
    Doctor.objects.create(name="Bailey", department=ortho, specialization="Orthopedic Surgeon", availability="Fri, 1PM-6PM")
    Doctor.objects.create(name="Bones", department=ortho, specialization="Sports Medicine", availability="Mon-Wed, 10AM-4PM")
    Disease.objects.create(name="Fracture", department=ortho, symptoms="severe acute pain, swelling, visible deformity, inability to move joint")
    Disease.objects.create(name="Osteoarthritis", department=ortho, symptoms="chronic joint pain, morning stiffness, reduced range of motion")
    Disease.objects.create(name="Sprained Ankle", department=ortho, symptoms="swelling, bruising, pain on walking")

    # Department 4: Dermatology
    derma = Department.objects.create(
        name="Dermatology",
        description="Specializes in skin, hair, and nail conditions.",
        keywords="skin rash itch acne redness burn mole hair loss spots blisters warts hives eczema psoriasis scaling dandruff peeling pigmentation cyst nail infection ulcer"
    )
    Doctor.objects.create(name="Grey", department=derma, specialization="Dermatologist", availability="Tue-Fri, 10AM-3PM")
    Disease.objects.create(name="Eczema", department=derma, symptoms="extremely itchy, red, dry, cracked skin patches")
    Disease.objects.create(name="Acne Vulgaris", department=derma, symptoms="pimples, oily skin, blackheads, scarring")
    Disease.objects.create(name="Melanoma", department=derma, symptoms="changing mole, irregular border, dark spots on skin")

    # Department 5: Gastroenterology
    gastro = Department.objects.create(
        name="Gastroenterology",
        description="Digestive system and its disorders.",
        keywords="stomach ache abdominal pain nausea vomiting diarrhea constipation bloating gas heartburn acid reflux bowel blood in stool indigestion ulcer liver pancreas digestion"
    )
    Doctor.objects.create(name="Watson", department=gastro, specialization="Gastroenterologist", availability="Mon, Wed, Fri 9AM-4PM")
    Disease.objects.create(name="GERD / Acid Reflux", department=gastro, symptoms="heartburn, acid taste in mouth, chest burning after eating")
    Disease.objects.create(name="Gastroenteritis", department=gastro, symptoms="watery diarrhea, abdominal cramps, nausea, vomiting")
    Disease.objects.create(name="IBS", department=gastro, symptoms="abdominal pain, bloating, alternating diarrhea and constipation")

    # Department 6: Pulmonology
    pulmo = Department.objects.create(
        name="Pulmonology",
        description="Respiratory tract conditions.",
        keywords="cough breathing lungs shortness of breath wheezing asthma asthma inhaler coughing blood phlegm chest tightness mucus choking smoke COPD"
    )
    Doctor.objects.create(name="Chase", department=pulmo, specialization="Pulmonologist", availability="Mon-Thu 8AM-12PM")
    Disease.objects.create(name="Asthma", department=pulmo, symptoms="wheezing, shortness of breath, chest tightness, night cough")
    Disease.objects.create(name="Pneumonia", department=pulmo, symptoms="wet cough, high fever, chills, difficulty breathing")
    Disease.objects.create(name="Bronchitis", department=pulmo, symptoms="persistent cough, thick mucus, chest discomfort")

    # Department 7: General Medicine / Pediatrics
    gen = Department.objects.create(
        name="General Medicine",
        description="Comprehensive healthcare and primary care.",
        keywords="fever cold flu temperature chill fatigue tired sore throat runny nose sneezing body ache weak weak malaise routine checkup virus bacterial infection vaccine"
    )
    Doctor.objects.create(name="Carter", department=gen, specialization="General Physician", availability="Everyday 9AM-5PM")
    Disease.objects.create(name="Influenza (Flu)", department=gen, symptoms="high fever, severe body aches, fatigue, dry cough")
    Disease.objects.create(name="Common Cold", department=gen, symptoms="runny nose, mild sore throat, sneezing, slight fatigue")
    Disease.objects.create(name="Strep Throat", department=gen, symptoms="severe sore throat, pain when swallowing, fever, swollen lymph nodes")

    print("Database seeded successfully with massive Keywords, Departments, Doctors, and Diseases.")

if __name__ == '__main__':
    seed()
