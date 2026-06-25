# MediSync: AI-Powered Hospital Management System

MediSync is a modern, professional Hospital Management System built with Django. It features a unique AI-driven specialist recommendation engine that uses Natural Language Processing (NLP) to match patient symptoms with the most appropriate medical departments.

## 🌟 Key Features
- **AI Recommendation Engine**: Uses TF-IDF and Cosine Similarity to analyze symptoms.
- **Role-Based Portals**: Dedicated interfaces for Admins, Doctors, and Patients.
- **Appointment Management**: Real-time booking and clinical approval workflow.
- **Semantic UI**: Modern, premium design system with 100% human-readable CSS.
- **Analytics Dashboard**: Overview of hospital operations for administrators.

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Frontend**: Vanilla HTML5, Semantic CSS3, JavaScript (ES6+)
- **AI/ML**: Scikit-Learn (TF-IDF, NLP)
- **Database**: MySQL (Production-ready)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- MySQL Server
- Virtual Environment (recommended)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/hospital-project.git
cd hospital-project
pip install -r requirements.txt
```

### 3. Database Configuration
1. **Create the Database**:
   Open your MySQL console and run:
   ```sql
   CREATE DATABASE hospital_db;
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory and add your credentials:
   ```env
   SECRET_KEY=your_key
   DEBUG=True
   DB_NAME=hospital_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

3. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. Running the Project
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## 📂 Project Structure for Contributors
- `/recommendation`: Main app logic and AI engine.
- `/static`: Premium CSS design system and frontend assets.
- `/templates`: Semantic HTML5 templates organized by user role.
- `/media`: Profiles and medical record uploads (Git-ignored).

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
