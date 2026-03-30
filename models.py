from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'Department'
    DepartmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name         = db.Column(db.String(100), nullable=False)
    Location     = db.Column(db.String(100))
    Phone        = db.Column(db.String(20), unique=True)

    doctors = db.relationship('Doctor', backref='department', lazy=True)
    rooms   = db.relationship('Room',   backref='department', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'Doctor'
    DoctorID      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name          = db.Column(db.String(100), nullable=False)
    Phone         = db.Column(db.String(20), unique=True)
    LicenseNumber = db.Column(db.String(50), unique=True, nullable=False)
    Specialty     = db.Column(db.String(100))
    DepartmentID  = db.Column(db.Integer, db.ForeignKey('Department.DepartmentID'))

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)


class Patient(db.Model):
    __tablename__ = 'Patient'
    PatientID         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name              = db.Column(db.String(100), nullable=False)
    DOB               = db.Column(db.Date)
    Gender            = db.Column(db.Enum('Male', 'Female', 'Other'))
    Phone             = db.Column(db.String(20), unique=True)
    Email             = db.Column(db.String(100), unique=True)
    Address           = db.Column(db.String(200))
    BloodType         = db.Column(db.String(5))
    InsuranceProvider = db.Column(db.String(100))
    PolicyNumber      = db.Column(db.String(50))

    appointments = db.relationship('Appointment', backref='patient', lazy=True)


class Room(db.Model):
    __tablename__ = 'Room'
    RoomID       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomNumber   = db.Column(db.String(20), nullable=False)
    Type         = db.Column(db.Enum('ICU', 'General', 'Surgery', 'Emergency'), nullable=False)
    Status       = db.Column(db.Enum('Available', 'Occupied', 'Maintenance'), default='Available')
    DepartmentID = db.Column(db.Integer, db.ForeignKey('Department.DepartmentID'))

    appointments = db.relationship('Appointment', backref='room', lazy=True)


class Appointment(db.Model):
    __tablename__ = 'Appointment'
    AppointmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date          = db.Column(db.Date, nullable=False)
    Time          = db.Column(db.Time, nullable=False)
    Reason        = db.Column(db.String(255))
    Status        = db.Column(db.Enum('Scheduled', 'Completed', 'Cancelled'), default='Scheduled')
    PatientID     = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'))
    DoctorID      = db.Column(db.Integer, db.ForeignKey('Doctor.DoctorID'))
    RoomID        = db.Column(db.Integer, db.ForeignKey('Room.RoomID'))

    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False, lazy=True)


class MedicalRecord(db.Model):
    __tablename__ = 'MedicalRecord'
    RecordID      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Diagnosis     = db.Column(db.String(255))
    Treatment     = db.Column(db.String(255))
    Notes         = db.Column(db.Text)
    Date          = db.Column(db.Date)
    AppointmentID = db.Column(db.Integer, db.ForeignKey('Appointment.AppointmentID'), unique=True)

    prescriptions = db.relationship('Prescribes', backref='record', lazy=True)


class Medication(db.Model):
    __tablename__ = 'Medication'
    MedicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name         = db.Column(db.String(100), nullable=False)
    Dosage       = db.Column(db.String(50))
    SideEffects  = db.Column(db.Text)
    Manufacturer = db.Column(db.String(100))

    prescriptions = db.relationship('Prescribes', backref='medication', lazy=True)


class Prescribes(db.Model):
    __tablename__ = 'Prescribes'
    RecordID     = db.Column(db.Integer, db.ForeignKey('MedicalRecord.RecordID'), primary_key=True)
    MedicationID = db.Column(db.Integer, db.ForeignKey('Medication.MedicationID'), primary_key=True)
    Instructions = db.Column(db.String(255))
