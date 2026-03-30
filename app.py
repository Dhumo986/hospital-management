from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Patient, Doctor, Department, Room, Appointment, MedicalRecord, Medication, Prescribes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ── Home ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    stats = {
        'patients':     Patient.query.count(),
        'doctors':      Doctor.query.count(),
        'appointments': Appointment.query.count(),
        'departments':  Department.query.count(),
    }
    return render_template('index.html', stats=stats)

# ══════════════════════════════════════════════════════════════════════════════
# PATIENT ROUTES (Shezan's module)
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/patients')
def patients():
    search = request.args.get('search', '')
    if search:
        results = Patient.query.filter(
            Patient.Name.ilike(f'%{search}%') |
            Patient.Phone.ilike(f'%{search}%')
        ).all()
    else:
        results = Patient.query.all()
    return render_template('patients.html', patients=results, search=search)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        p = Patient(
            Name=request.form['name'],
            DOB=request.form['dob'] or None,
            Gender=request.form['gender'],
            Phone=request.form['phone'],
            Email=request.form['email'],
            Address=request.form['address'],
            BloodType=request.form['blood_type'],
            InsuranceProvider=request.form['insurance_provider'],
            PolicyNumber=request.form['policy_number']
        )
        db.session.add(p)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    p = Patient.query.get_or_404(id)
    if request.method == 'POST':
        p.Name              = request.form['name']
        p.Phone             = request.form['phone']
        p.Email             = request.form['email']
        p.Address           = request.form['address']
        p.InsuranceProvider = request.form['insurance_provider']
        p.PolicyNumber      = request.form['policy_number']
        db.session.commit()
        flash('Patient updated!', 'success')
        return redirect(url_for('patients'))
    return render_template('edit_patient.html', patient=p)

@app.route('/patients/delete/<int:id>')
def delete_patient(id):
    p = Patient.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Patient deleted.', 'warning')
    return redirect(url_for('patients'))

# ══════════════════════════════════════════════════════════════════════════════
# DOCTOR ROUTES (Dhruv's module)
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/doctors')
def doctors():
    search = request.args.get('search', '')
    if search:
        results = Doctor.query.filter(
            Doctor.Name.ilike(f'%{search}%') |
            Doctor.Specialty.ilike(f'%{search}%')
        ).all()
    else:
        results = Doctor.query.all()
    return render_template('doctors.html', doctors=results, search=search)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    departments = Department.query.all()
    if request.method == 'POST':
        d = Doctor(
            Name=request.form['name'],
            Phone=request.form['phone'],
            LicenseNumber=request.form['license_number'],
            Specialty=request.form['specialty'],
            DepartmentID=request.form['department_id']
        )
        db.session.add(d)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html', departments=departments)

@app.route('/doctors/edit/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    d = Doctor.query.get_or_404(id)
    departments = Department.query.all()
    if request.method == 'POST':
        d.Name         = request.form['name']
        d.Phone        = request.form['phone']
        d.Specialty    = request.form['specialty']
        d.DepartmentID = request.form['department_id']
        db.session.commit()
        flash('Doctor updated!', 'success')
        return redirect(url_for('doctors'))
    return render_template('edit_doctor.html', doctor=d, departments=departments)

@app.route('/doctors/delete/<int:id>')
def delete_doctor(id):
    d = Doctor.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash('Doctor deleted.', 'warning')
    return redirect(url_for('doctors'))

# ══════════════════════════════════════════════════════════════════════════════
# APPOINTMENT ROUTES (Rafik's module)
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/appointments')
def appointments():
    results = Appointment.query.all()
    return render_template('appointments.html', appointments=results)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    patients = Patient.query.all()
    doctors  = Doctor.query.all()
    rooms    = Room.query.filter_by(Status='Available').all()
    if request.method == 'POST':
        a = Appointment(
            Date=request.form['date'],
            Time=request.form['time'],
            Reason=request.form['reason'],
            Status='Scheduled',
            PatientID=request.form['patient_id'],
            DoctorID=request.form['doctor_id'],
            RoomID=request.form['room_id']
        )
        db.session.add(a)
        db.session.commit()
        flash('Appointment scheduled!', 'success')
        return redirect(url_for('appointments'))
    return render_template('add_appointment.html', patients=patients, doctors=doctors, rooms=rooms)

@app.route('/appointments/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    a = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        a.Status = request.form['status']
        db.session.commit()
        flash('Appointment updated!', 'success')
        return redirect(url_for('appointments'))
    return render_template('edit_appointment.html', appointment=a)

@app.route('/appointments/delete/<int:id>')
def delete_appointment(id):
    a = Appointment.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Appointment deleted.', 'warning')
    return redirect(url_for('appointments'))

# ══════════════════════════════════════════════════════════════════════════════
# MEDICATION ROUTES (Dhruv's module)
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/medications')
def medications():
    results = Medication.query.all()
    return render_template('medications.html', medications=results)

@app.route('/medications/add', methods=['GET', 'POST'])
def add_medication():
    if request.method == 'POST':
        m = Medication(
            Name=request.form['name'],
            Dosage=request.form['dosage'],
            SideEffects=request.form['side_effects'],
            Manufacturer=request.form['manufacturer']
        )
        db.session.add(m)
        db.session.commit()
        flash('Medication added!', 'success')
        return redirect(url_for('medications'))
    return render_template('add_medication.html')

# ══════════════════════════════════════════════════════════════════════════════
# DEPARTMENT ROUTES (Dhruv's module)
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/departments')
def departments():
    results = Department.query.all()
    return render_template('departments.html', departments=results)

# ══════════════════════════════════════════════════════════════════════════════
# ADVANCED FEATURE: Smart Doctor Recommendation
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    recommended = []
    if request.method == 'POST':
        specialty = request.form['specialty']
        date      = request.form['date']
        time      = request.form['time']

        # Get doctors matching specialty
        matched_doctors = Doctor.query.filter(
            Doctor.Specialty.ilike(f'%{specialty}%')
        ).all()

        # Filter out doctors who already have an appointment at that date/time
        for doctor in matched_doctors:
            conflict = Appointment.query.filter_by(
                DoctorID=doctor.DoctorID,
                Date=date,
                Time=time,
                Status='Scheduled'
            ).first()
            if not conflict:
                recommended.append(doctor)

    specialties = db.session.query(Doctor.Specialty).distinct().all()
    specialties = [s[0] for s in specialties]
    return render_template('recommend.html', recommended=recommended, specialties=specialties)


if __name__ == '__main__':
    app.run(debug=True)
