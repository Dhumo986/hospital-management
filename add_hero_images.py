import os

# Update index.html with hospital hero banner
index = '''{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block page_title %}Dashboard{% endblock %}

{% block content %}

<!-- Hero Banner -->
<div style="
  background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.6)),
  url('https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=1200&q=80') center/cover no-repeat;
  border-radius: 12px;
  padding: 48px 36px;
  margin-bottom: 28px;
  color: white;
">
  <h1 style="font-size:28px;font-weight:700;margin-bottom:8px;letter-spacing:-0.5px">Welcome to Hospital MS</h1>
  <p style="font-size:14px;opacity:0.85;max-width:500px">A centralized platform for managing patients, doctors, appointments, and medical records at Florida State University — Team 32, COP 4710.</p>
</div>

<div class="stats-grid">
  <div class="stat-card"><div class="stat-icon">👤</div><div class="stat-label">Total Patients</div><div class="stat-value">{{ stats.patients }}</div></div>
  <div class="stat-card"><div class="stat-icon">🩺</div><div class="stat-label">Total Doctors</div><div class="stat-value">{{ stats.doctors }}</div></div>
  <div class="stat-card"><div class="stat-icon">📅</div><div class="stat-label">Appointments</div><div class="stat-value">{{ stats.appointments }}</div></div>
  <div class="stat-card"><div class="stat-icon">🏥</div><div class="stat-label">Departments</div><div class="stat-value">{{ stats.departments }}</div></div>
</div>

<div class="card"><div class="card-header"><h2>Quick Navigation</h2></div>
<div class="card-body"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
  <a href="/patients/add" class="btn btn-primary">+ Add Patient</a>
  <a href="/doctors/add" class="btn btn-primary">+ Add Doctor</a>
  <a href="/appointments/add" class="btn btn-primary">+ Schedule Appointment</a>
  <a href="/medications/add" class="btn btn-outline">+ Add Medication</a>
  <a href="/recommend" class="btn btn-success">⭐ Recommend Doctor</a>
</div></div></div>
{% endblock %}'''

# Update doctors.html with doctor hero banner
doctors = '''{% extends "base.html" %}
{% block title %}Doctors{% endblock %}
{% block page_title %}Doctors{% endblock %}
{% block topbar_actions %}<a href="/doctors/add" class="btn btn-primary">+ Add Doctor</a>{% endblock %}

{% block content %}

<div style="
  background: linear-gradient(rgba(0,40,80,0.7), rgba(0,40,80,0.8)),
  url('https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=1200&q=80') center/cover no-repeat;
  border-radius: 12px;
  padding: 36px;
  margin-bottom: 24px;
  color: white;
">
  <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">Our Medical Team</h1>
  <p style="font-size:13.5px;opacity:0.85">Browse, search, and manage all doctors across departments.</p>
</div>

<div class="card">
  <div class="card-header">
    <h2>All Doctors ({{ doctors|length }})</h2>
    <form method="GET" action="/doctors" class="search-bar" style="margin:0">
      <input name="search" placeholder="Search by name or specialty..." value="{{ search }}"/>
      <button type="submit" class="btn btn-outline">Search</button>
      {% if search %}<a href="/doctors" class="btn btn-outline">Clear</a>{% endif %}
    </form>
  </div>
  <div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Name</th><th>Specialty</th><th>License</th><th>Phone</th><th>Department</th><th>Actions</th></tr></thead>
    <tbody>
    {% for d in doctors %}
    <tr>
      <td><span style="font-family:\'DM Mono\',monospace;color:var(--text-muted)">#{{ d.DoctorID }}</span></td>
      <td><strong>{{ d.Name }}</strong></td>
      <td><span class="badge badge-blue">{{ d.Specialty or "—" }}</span></td>
      <td><span style="font-family:\'DM Mono\',monospace;font-size:12px">{{ d.LicenseNumber }}</span></td>
      <td>{{ d.Phone or "—" }}</td>
      <td>{{ d.department.Name if d.department else "—" }}</td>
      <td style="display:flex;gap:6px">
        <a href="/doctors/edit/{{ d.DoctorID }}" class="btn btn-sm btn-outline">Edit</a>
        <a href="/doctors/delete/{{ d.DoctorID }}" class="btn btn-sm btn-danger" onclick="return confirm(\'Delete?\')">Delete</a>
      </td>
    </tr>
    {% else %}<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:32px">No doctors found.</td></tr>{% endfor %}
    </tbody>
  </table></div>
</div>
{% endblock %}'''

# Update patients.html with patient hero banner
patients = '''{% extends "base.html" %}
{% block title %}Patients{% endblock %}
{% block page_title %}Patients{% endblock %}
{% block topbar_actions %}<a href="/patients/add" class="btn btn-primary">+ Add Patient</a>{% endblock %}

{% block content %}

<div style="
  background: linear-gradient(rgba(0,60,40,0.7), rgba(0,60,40,0.8)),
  url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=1200&q=80') center/cover no-repeat;
  border-radius: 12px;
  padding: 36px;
  margin-bottom: 24px;
  color: white;
">
  <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">Patient Registry</h1>
  <p style="font-size:13.5px;opacity:0.85">Search and manage all registered patients in the system.</p>
</div>

<div class="card">
  <div class="card-header">
    <h2>All Patients ({{ patients|length }})</h2>
    <form method="GET" action="/patients" class="search-bar" style="margin:0">
      <input name="search" placeholder="Search by name or phone..." value="{{ search }}"/>
      <button type="submit" class="btn btn-outline">Search</button>
      {% if search %}<a href="/patients" class="btn btn-outline">Clear</a>{% endif %}
    </form>
  </div>
  <div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Name</th><th>DOB</th><th>Gender</th><th>Phone</th><th>Blood Type</th><th>Insurance</th><th>Actions</th></tr></thead>
    <tbody>
    {% for p in patients %}
    <tr>
      <td><span style="font-family:\'DM Mono\',monospace;color:var(--text-muted)">#{{ p.PatientID }}</span></td>
      <td><strong>{{ p.Name }}</strong></td>
      <td>{{ p.DOB or "—" }}</td>
      <td>{% if p.Gender == "Male" %}<span class="badge badge-blue">Male</span>{% elif p.Gender == "Female" %}<span class="badge badge-green">Female</span>{% else %}<span class="badge badge-gray">Other</span>{% endif %}</td>
      <td>{{ p.Phone or "—" }}</td>
      <td><span class="badge badge-yellow">{{ p.BloodType or "—" }}</span></td>
      <td>{{ p.InsuranceProvider or "—" }}</td>
      <td style="display:flex;gap:6px">
        <a href="/patients/edit/{{ p.PatientID }}" class="btn btn-sm btn-outline">Edit</a>
        <a href="/patients/delete/{{ p.PatientID }}" class="btn btn-sm btn-danger" onclick="return confirm(\'Delete this patient?\')">Delete</a>
      </td>
    </tr>
    {% else %}<tr><td colspan="8" style="text-align:center;color:var(--text-muted);padding:32px">No patients found.</td></tr>{% endfor %}
    </tbody>
  </table></div>
</div>
{% endblock %}'''

# Update appointments.html with hero banner
appointments = '''{% extends "base.html" %}
{% block title %}Appointments{% endblock %}
{% block page_title %}Appointments{% endblock %}
{% block topbar_actions %}<a href="/appointments/add" class="btn btn-primary">+ Schedule Appointment</a>{% endblock %}

{% block content %}

<div style="
  background: linear-gradient(rgba(60,0,80,0.7), rgba(60,0,80,0.8)),
  url('https://images.unsplash.com/photo-1631217868264-e5b90bb7e133?w=1200&q=80') center/cover no-repeat;
  border-radius: 12px;
  padding: 36px;
  margin-bottom: 24px;
  color: white;
">
  <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">Appointments</h1>
  <p style="font-size:13.5px;opacity:0.85">Schedule, manage, and track all patient appointments.</p>
</div>

<div class="card">
  <div class="card-header"><h2>All Appointments ({{ appointments|length }})</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Date</th><th>Time</th><th>Patient</th><th>Doctor</th><th>Room</th><th>Reason</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>
    {% for a in appointments %}
    <tr>
      <td><span style="font-family:\'DM Mono\',monospace;color:var(--text-muted)">#{{ a.AppointmentID }}</span></td>
      <td>{{ a.Date }}</td><td>{{ a.Time }}</td>
      <td>{{ a.patient.Name if a.patient else "—" }}</td>
      <td>{{ a.doctor.Name if a.doctor else "—" }}</td>
      <td>{{ a.room.RoomNumber if a.room else "—" }}</td>
      <td>{{ a.Reason or "—" }}</td>
      <td>{% if a.Status == "Scheduled" %}<span class="badge badge-blue">Scheduled</span>{% elif a.Status == "Completed" %}<span class="badge badge-green">Completed</span>{% else %}<span class="badge badge-red">Cancelled</span>{% endif %}</td>
      <td style="display:flex;gap:6px">
        <a href="/appointments/edit/{{ a.AppointmentID }}" class="btn btn-sm btn-outline">Edit</a>
        <a href="/appointments/delete/{{ a.AppointmentID }}" class="btn btn-sm btn-danger" onclick="return confirm(\'Delete?\')">Delete</a>
      </td>
    </tr>
    {% else %}<tr><td colspan="9" style="text-align:center;color:var(--text-muted);padding:32px">No appointments found.</td></tr>{% endfor %}
    </tbody>
  </table></div>
</div>
{% endblock %}'''

# Write all files
templates_dir = '/Users/dhruvupadhyay/hospital-management/templates'

with open(f'{templates_dir}/index.html', 'w') as f:
    f.write(index)
print("✓ index.html updated")

with open(f'{templates_dir}/doctors.html', 'w') as f:
    f.write(doctors)
print("✓ doctors.html updated")

with open(f'{templates_dir}/patients.html', 'w') as f:
    f.write(patients)
print("✓ patients.html updated")

with open(f'{templates_dir}/appointments.html', 'w') as f:
    f.write(appointments)
print("✓ appointments.html updated")

print("\nDone! Restart Flask: python3 app.py")
