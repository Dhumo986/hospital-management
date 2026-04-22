# Report of Contribution
**Project:** Hospital Management System  
**Course:** COP 4710 — Theory and Structure of Databases, Spring 2026  
**Team:** 32  

---

## Team Members & Contributions

### Dhruv Upadhyay (DTU24) — [@Dhumo986](https://github.com/Dhumo986)

**Modules Owned:**
- Doctor module (list, add, edit, delete, search by name/specialty)
- Medication module (list, add)
- Department module (list with doctor and room counts)
- Smart Doctor Recommendation (advanced feature)
- Stats & Reports page (aggregate queries)

**Technical Contributions:**
- Set up the entire project infrastructure (Flask app, SQLAlchemy models, Railway MySQL database)
- Wrote `app.py` with all routes and application logic
- Wrote `models.py` with all 8 SQLAlchemy models
- Created all 15 HTML templates with base layout and sidebar navigation
- Wrote `schema.sql` to create all 8 database tables
- Wrote `fake_data.py` to populate the database with 100 patients, 20 doctors, 200 appointments, 50 medications, and prescriptions using Python Faker
- Set up GitHub repository and connected Railway cloud MySQL database
- Implemented Smart Doctor Recommendation feature using multi-table joins and scheduling conflict detection
- Implemented Stats & Reports page with 4 aggregate queries (appointments per doctor, appointments by status, patients per department, most prescribed medications)
- Wrote README.md and project documentation

---

### Rafik Taleb (RT24E) — [@Rafik-taleb](https://github.com/Rafik-taleb)

**Modules Owned:**
- Appointments module (list, add, edit status, delete)
- Room management (room availability, room assignment during booking)

**Technical Contributions:**
- Implemented appointment scheduling with patient, doctor, and room selection
- Implemented appointment status updates (Scheduled → Completed/Cancelled)
- Managed room availability logic during appointment creation
- Tested and verified appointment-related database queries

---

### Shezan Abdul Mujeer Chisty (SA24BD) — [@shezanch](https://github.com/shezanch)

**Modules Owned:**
- Patient module (list, add, edit, delete, search)
- Medical Records module (view, add)

**Technical Contributions:**
- Implemented patient registration with full demographic and insurance information
- Implemented patient search by name and phone number
- Implemented medical records creation linked to completed appointments
- Tested and verified patient and medical record database queries

---

## Collaboration

All three members collaborated on:
- Final integration and testing of all modules
- Demo preparation and rehearsal
- Final report writing
- Code review via GitHub pull requests

---

## Labor Distribution Summary

| Task | Dhruv | Rafik | Shezan |
|------|-------|-------|--------|
| Project setup & infrastructure | ✅ | | |
| Database schema & fake data | ✅ | | |
| Flask app & models | ✅ | | |
| HTML templates & UI | ✅ | | |
| Doctor module | ✅ | | |
| Medication module | ✅ | | |
| Department module | ✅ | | |
| Appointment module | | ✅ | |
| Room management | | ✅ | |
| Patient module | | | ✅ |
| Medical Records | | | ✅ |
| Smart Doctor Recommendation | ✅ | | |
| Stats & Reports | ✅ | | |
| README & documentation | ✅ | | |
| Final report | ✅ | ✅ | ✅ |
| Demo | ✅ | ✅ | ✅ |
