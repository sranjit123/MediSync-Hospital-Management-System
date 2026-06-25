# Hospital Management System: Project Documentation

This document details the data flow, entity relationships, and database structure for the Hospital Management System.

---

## 1. Data Flow Diagrams (DFD)

### DFD Level 0 (Context Diagram)
Visualizes high-level system interactions.

```mermaid
graph LR
    P[Patient] -- "Symptoms / Requests" --> HMS["Hospital Management System"]
    P -- "Signup/Login" --> HMS
    HMS -- "Doctor Recommendations" --> P
    HMS -- "Appointment Status" --> P

    D[Doctor] -- "Availability / Actions" --> HMS
    D -- "Signup/Login" --> HMS
    HMS -- "Patient Appointments" --> D
    HMS -- "Dashboard Stats" --> D

    A[Admin] -- "Dept/Doctor/Disease Management" --> HMS
    HMS -- "System Overviews / Reports" --> A
```

---

### DFD Level 1
Breaks down the core sub-processes of the application.

```mermaid
graph TD
    subgraph "Hospital Management System"
        P1["P1: Auth & Role Control"]
        P2["P2: AI Symptom Processing"]
        P3["P3: Appointment Workflow"]
        P4["P4: Resource Management"]
    end

    Patient -- "Login/Signup" --> P1
    Doctor -- "Login/Signup" --> P1
    Admin -- "Login/Signup" --> P1

    Patient -- "Symptoms" --> P2
    P2 -- "Match Results" --> Patient

    Patient -- "Book Request" --> P3
    P3 -- "Availability Check" --> Doctor
    Doctor -- "Accept/Reject" --> P3
    P3 -- "Status Update" --> Patient

    Admin -- "Update Depts/Doctors" --> P4
    P4 -- "Sync DB" --> P2
```

---

## 2. Entity Relationship (ER) Diagram
Details the 3-table inheritance model and medical relationships.

```mermaid
erDiagram
    users {
        int id PK
        string username
        string password
        string email
        string full_name
        string role
    }
    admin {
        int id PK, FK
    }
    doctor {
        int id PK, FK
        string specialization
        text availability
        int department_id FK
    }
    patient {
        int id PK, FK
    }
    department {
        int id PK
        string name
        text description
        text keywords
    }
    disease {
        int id PK
        string name
        text symptoms
        int department_id FK
    }
    appointment {
        int id PK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time appointment_time
        string status
    }

    users ||--|| admin : "IS-A"
    users ||--|| doctor : "IS-A"
    users ||--|| patient : "IS-A"
    doctor }o--|| department : "Belongs To"
    disease }o--|| department : "Categorized By"
    appointment }o--|| patient : "Booked By"
    appointment }o--|| doctor : "Attended By"
```

---

## 3. Database Schemas
Flat SQL table definitions for the current implementation.

### Table: `users`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `username` | VARCHAR(150)| UNIQUE, NOT NULL |
| `password` | VARCHAR(128)| NOT NULL (Hashed) |
| `email` | VARCHAR(254)| NOT NULL |
| `full_name` | VARCHAR(200)| |
| `role` | VARCHAR(10) | 'admin', 'doctor', 'patient' |
| `image` | VARCHAR(100)| NULLABLE (Path to media) |

### Table: `doctor`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, FOREIGN KEY (`users.id`) |
| `department_id`| INT | FOREIGN KEY (`department.id`) |
| `specialization`| VARCHAR(200)| |
| `availability`| TEXT | (e.g. "Mon-Fri 09:00-17:00") |

### Table: `patient`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, FOREIGN KEY (`users.id`) |

### Table: `admin`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, FOREIGN KEY (`users.id`) |

### Table: `appointment`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `patient_id` | INT | FOREIGN KEY (`patient.id`) |
| `doctor_id` | INT | FOREIGN KEY (`doctor.id`) |
| `appointment_date`| DATE | |
| `appointment_time`| TIME | |
| `status` | VARCHAR(10) | Default: 'pending' |
| `symptoms` | TEXT | |

### Table: `department`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `name` | VARCHAR(100)| UNIQUE |
| `description` | TEXT | |
| `keywords` | TEXT | (Symptom words for AI) |
