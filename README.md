# 🏥 Hospital Management System
> COP 4710: Theory and Structure of Databases — Spring 2026  
> Florida State University | Team 32

## Team Members
| Name | FSU ID | GitHub |
|------|--------|--------|
| Rafik Taleb | RT24E | [@Rafik-taleb](https://github.com/Rafik-taleb) |
| Shezan Abdul Mujeer Chisty | SA24BD | [@shezanch](https://github.com/shezanch) |
| Dhruv Upadhyay | DTU24 | [@Dhumo986](https://github.com/Dhumo986) |

---

## 📋 Project Overview
A web-based Hospital Management System built with Flask and MySQL that manages patients, doctors, departments, appointments, medical records, and medications. The system provides a centralized platform for hospital staff to manage core operations efficiently.

---

## 🗄️ Database
- **Platform:** MySQL (hosted on Railway)
- **Tables:** Patient, Doctor, Department, Room, Appointment, MedicalRecord, Medication, Prescribes (8 total)

### Entity Relationship
- A **Patient** books many **Appointments**
- A **Doctor** handles many **Appointments**
- An **Appointment** uses one **Room** and generates one **MedicalRecord**
- A **MedicalRecord** prescribes many **Medications** (via Prescribes bridge table)
- **Doctors** and **Rooms** belong to **Departments**

---

## ⚙️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| Database | MySQL via Railway |
| ORM | SQLAlchemy |
| Frontend | HTML/CSS + Jinja2 |
| Data Generation | Python Faker |

---

## 🚀 Features

### Basic Functions
- ✅ Insert — Add patients, doctors, appointments, medications
- ✅ Search — Search patients by name/phone, doctors by specialty
- ✅ Join Query — Appointments page joins Patient, Doctor, and Room tables
- ✅ Aggregate Query — Stats page shows appointments per doctor, patients per department
- ✅ Update — Edit appointment status, patient info, doctor info
- ✅ Delete — Remove patients, doctors, appointments

### Advanced Feature — Smart Doctor Recommendation
When a patient needs an appointment, instead of manually browsing doctors, the system automatically recommends available doctors by:
- Matching the patient's required specialty to doctors
- Checking for scheduling conflicts at the requested date and time
- Returning a ranked list of available doctors

---

## 📁 Project Structure
```
hospital-management/
├── app.py              # Flask routes and application logic
├── models.py           # SQLAlchemy database models
├── .env                # Database credentials (not committed)
├── .gitignore
├── templates/
│   ├── base.html           # Base layout with sidebar
│   ├── index.html          # Dashboard
│   ├── patients.html       # Patient list
│   ├── add_patient.html    # Add patient form
│   ├── edit_patient.html   # Edit patient form
│   ├── doctors.html        # Doctor list
│   ├── add_doctor.html     # Add doctor form
│   ├── edit_doctor.html    # Edit doctor form
│   ├── appointments.html   # Appointment list
│   ├── add_appointment.html
│   ├── edit_appointment.html
│   ├── medications.html    # Medication list
│   ├── add_medication.html
│   ├── departments.html    # Department list
│   ├── recommend.html      # Smart Doctor Recommendation
│   └── stats.html          # Aggregate queries & reports
└── static/
```

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Dhumo986/hospital-management.git
cd hospital-management
```

**2. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install flask sqlalchemy pymysql python-dotenv cryptography flask-sqlalchemy
```

**4. Set up environment variables**

Create a `.env` file in the project root (get credentials from team):
```
DB_HOST=gondola.proxy.rlwy.net
DB_PORT=33433
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=railway
```

**5. Run the application**
```bash
python3 app.py
```

**6. Open in browser**
```
http://127.0.0.1:5000
```

---

## 📊 Key SQL Queries

### Join Query — Appointments with Patient, Doctor, Room
```sql
SELECT a.AppointmentID, a.Date, a.Time, a.Status,
       p.Name AS Patient, d.Name AS Doctor, r.RoomNumber
FROM Appointment a
JOIN Patient p ON a.PatientID = p.PatientID
JOIN Doctor d ON a.DoctorID = d.DoctorID
JOIN Room r ON a.RoomID = r.RoomID;
```

### Aggregate Query — Appointments per Doctor
```sql
SELECT d.Name, d.Specialty, COUNT(a.AppointmentID) AS Total
FROM Doctor d
JOIN Appointment a ON d.DoctorID = a.DoctorID
GROUP BY d.DoctorID
ORDER BY Total DESC;
```

### Aggregate Query — Unique Patients per Department
```sql
SELECT dept.Name, COUNT(DISTINCT a.PatientID) AS Patients
FROM Department dept
JOIN Doctor d ON dept.DepartmentID = d.DepartmentID
JOIN Appointment a ON d.DoctorID = a.DoctorID
GROUP BY dept.DepartmentID
ORDER BY Patients DESC;
```

---

## 👥 Labor Division
| Member                     | Modules                       |
|----------------------------|-------------------------------|
| Rafik Taleb                | Appointments, Room Management |
| Shezan Abdul Mujeer Chisty | Patients, Medical Records     |
| Dhruv Upadhyay             | Doctors, Medications, Departments, Smart Doctor Recommendation, Stats & Reports |

---

## 📅 Timeline
| Milestone | Date |
|-----------|------|
| Stage 2: ER Diagram | Feb 27, 2026 |
| Stage 3: Development Plan | Mar 13, 2026 |
| Database + Fake Data | Mar 30, 2026 |
| Flask App + Templates | Apr 5, 2026 |
| Advanced Feature | Apr 10, 2026 |
| Stats & Reports | Apr 14, 2026 |
| Demo + Final Report | Apr 24, 2026 |
