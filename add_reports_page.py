import os

template = '''{% extends "base.html" %}
{% block title %}Reports & Insights{% endblock %}
{% block page_title %}Reports & Insights{% endblock %}

{% block content %}

<!-- JOIN QUERIES SECTION -->
<div class="card" style="margin-bottom:24px">
  <div class="card-header">
    <h2>🔗 Join Queries</h2>
  </div>
  <div class="card-body">
    <p style="color:var(--text-muted);margin-bottom:20px;font-size:13.5px">
      These reports combine data from multiple tables to give you a complete picture.
    </p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">

      <!-- Join Query 1 -->
      <div class="card" style="border:1px solid var(--border)">
        <div class="card-header" style="background:var(--primary-light)">
          <h2 style="color:var(--primary)">📅 Full Appointment Details</h2>
        </div>
        <div class="card-body">
          <p style="color:var(--text-muted);font-size:13px;margin-bottom:16px">
            Shows every appointment with the patient name, doctor name, specialty, and room number — all in one view.
          </p>
          <form method="POST" action="/reports">
            <input type="hidden" name="query_type" value="appointments_full"/>
            <div class="form-group" style="margin-bottom:12px">
              <label>Filter by Status (optional)</label>
              <select name="status">
                <option value="">All Statuses</option>
                <option>Scheduled</option>
                <option>Completed</option>
                <option>Cancelled</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%">🔍 Run Report</button>
          </form>
        </div>
      </div>

      <!-- Join Query 2 -->
      <div class="card" style="border:1px solid var(--border)">
        <div class="card-header" style="background:var(--primary-light)">
          <h2 style="color:var(--primary)">🧾 Patient Medical History</h2>
        </div>
        <div class="card-body">
          <p style="color:var(--text-muted);font-size:13px;margin-bottom:16px">
            Look up a patient by name and see all their appointments, doctors visited, diagnoses, and treatments.
          </p>
          <form method="POST" action="/reports">
            <input type="hidden" name="query_type" value="patient_history"/>
            <div class="form-group" style="margin-bottom:12px">
              <label>Patient Name (or part of name)</label>
              <input name="patient_name" placeholder="e.g. John" required/>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%">🔍 Search History</button>
          </form>
        </div>
      </div>

    </div>
  </div>
</div>

<!-- AGGREGATE QUERIES SECTION -->
<div class="card" style="margin-bottom:24px">
  <div class="card-header">
    <h2>📊 Aggregate Reports</h2>
  </div>
  <div class="card-body">
    <p style="color:var(--text-muted);margin-bottom:20px;font-size:13.5px">
      These reports summarize and count data across the entire database.
    </p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">

      <!-- Aggregate Query 1 -->
      <div class="card" style="border:1px solid var(--border)">
        <div class="card-header" style="background:#f0fff4">
          <h2 style="color:#276749">🩺 Busiest Doctors</h2>
        </div>
        <div class="card-body">
          <p style="color:var(--text-muted);font-size:13px;margin-bottom:16px">
            Ranks all doctors by total number of appointments. Shows who handles the most patients.
          </p>
          <form method="POST" action="/reports">
            <input type="hidden" name="query_type" value="busiest_doctors"/>
            <div class="form-group" style="margin-bottom:12px">
              <label>Filter by Specialty (optional)</label>
              <select name="specialty">
                <option value="">All Specialties</option>
                <option>Cardiologist</option>
                <option>Neurologist</option>
                <option>Orthopedic Surgeon</option>
                <option>Emergency Physician</option>
                <option>General Practitioner</option>
              </select>
            </div>
            <button type="submit" class="btn btn-success" style="width:100%">📊 Run Report</button>
          </form>
        </div>
      </div>

      <!-- Aggregate Query 2 -->
      <div class="card" style="border:1px solid var(--border)">
        <div class="card-header" style="background:#fffbeb">
          <h2 style="color:#744210">🏥 Department Patient Load</h2>
        </div>
        <div class="card-body">
          <p style="color:var(--text-muted);font-size:13px;margin-bottom:16px">
            Shows how many unique patients each department has served. Helps identify which departments are most active.
          </p>
          <form method="POST" action="/reports">
            <input type="hidden" name="query_type" value="dept_load"/>
            <button type="submit" class="btn btn-outline" style="width:100%;border-color:#d69e2e;color:#744210">📊 Run Report</button>
          </form>
        </div>
      </div>

    </div>
  </div>
</div>

<!-- RESULTS -->
{% if results is not none %}
<div class="card">
  <div class="card-header">
    <h2>{{ result_title }} — {{ results|length }} rows</h2>
  </div>
  {% if results %}
  <div class="table-wrap"><table>
    <thead><tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr></thead>
    <tbody>
    {% for row in results %}
    <tr>{% for cell in row %}<td>{{ cell if cell is not none else "—" }}</td>{% endfor %}</tr>
    {% endfor %}
    </tbody>
  </table></div>
  {% else %}
  <div class="card-body" style="text-align:center;color:var(--text-muted);padding:32px">No results found.</div>
  {% endif %}
</div>
{% endif %}

{% if error %}
<div class="alert alert-danger">{{ error }}</div>
{% endif %}

{% endblock %}'''

with open('/Users/dhruvupadhyay/hospital-management/templates/reports.html', 'w') as f:
    f.write(template)
print("✓ reports.html created")

# Add sidebar link
base_path = '/Users/dhruvupadhyay/hospital-management/templates/base.html'
content = open(base_path).read()
if '/reports' not in content:
    content = content.replace('  </nav>', '    <a href="/reports"><span class="icon">📋</span> Reports</a>\n  </nav>')
    open(base_path, 'w').write(content)
    print("✓ sidebar link added")
else:
    print("✓ sidebar link already exists")

# Add route to app.py
app_path = '/Users/dhruvupadhyay/hospital-management/app.py'
app_content = open(app_path).read()

route = '''
# ══════════════════════════════════════════════════════════════════════════════
# REPORTS — User Friendly Query Interface
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    from sqlalchemy import text
    results = None
    columns = []
    error = None
    result_title = ""

    if request.method == 'POST':
        query_type = request.form.get('query_type')

        try:
            with db.engine.connect() as conn:

                # JOIN QUERY 1: Full Appointment Details
                if query_type == 'appointments_full':
                    status = request.form.get('status', '')
                    result_title = "Full Appointment Details"
                    if status:
                        sql = text("""
                            SELECT a.AppointmentID, a.Date, a.Time, a.Status,
                                   p.Name AS Patient, d.Name AS Doctor,
                                   d.Specialty, r.RoomNumber, r.Type AS RoomType
                            FROM Appointment a
                            JOIN Patient p ON a.PatientID = p.PatientID
                            JOIN Doctor d ON a.DoctorID = d.DoctorID
                            JOIN Room r ON a.RoomID = r.RoomID
                            WHERE a.Status = :status
                            ORDER BY a.Date DESC
                            LIMIT 50
                        """)
                        result = conn.execute(sql, {"status": status})
                    else:
                        sql = text("""
                            SELECT a.AppointmentID, a.Date, a.Time, a.Status,
                                   p.Name AS Patient, d.Name AS Doctor,
                                   d.Specialty, r.RoomNumber, r.Type AS RoomType
                            FROM Appointment a
                            JOIN Patient p ON a.PatientID = p.PatientID
                            JOIN Doctor d ON a.DoctorID = d.DoctorID
                            JOIN Room r ON a.RoomID = r.RoomID
                            ORDER BY a.Date DESC
                            LIMIT 50
                        """)
                        result = conn.execute(sql)
                    columns = list(result.keys())
                    results = [list(row) for row in result.fetchall()]

                # JOIN QUERY 2: Patient Medical History
                elif query_type == 'patient_history':
                    name = request.form.get('patient_name', '')
                    result_title = f"Medical History for patients matching: {name}"
                    sql = text("""
                        SELECT p.Name AS Patient, a.Date, a.Reason, a.Status,
                               d.Name AS Doctor, d.Specialty,
                               COALESCE(mr.Diagnosis, 'No record') AS Diagnosis,
                               COALESCE(mr.Treatment, 'No record') AS Treatment
                        FROM Patient p
                        JOIN Appointment a ON p.PatientID = a.PatientID
                        JOIN Doctor d ON a.DoctorID = d.DoctorID
                        LEFT JOIN MedicalRecord mr ON a.AppointmentID = mr.AppointmentID
                        WHERE p.Name LIKE :name
                        ORDER BY a.Date DESC
                        LIMIT 50
                    """)
                    result = conn.execute(sql, {"name": f"%{name}%"})
                    columns = list(result.keys())
                    results = [list(row) for row in result.fetchall()]

                # AGGREGATE QUERY 1: Busiest Doctors
                elif query_type == 'busiest_doctors':
                    specialty = request.form.get('specialty', '')
                    result_title = "Busiest Doctors by Appointment Count"
                    if specialty:
                        sql = text("""
                            SELECT d.Name AS Doctor, d.Specialty,
                                   dept.Name AS Department,
                                   COUNT(a.AppointmentID) AS TotalAppointments
                            FROM Doctor d
                            JOIN Appointment a ON d.DoctorID = a.DoctorID
                            JOIN Department dept ON d.DepartmentID = dept.DepartmentID
                            WHERE d.Specialty = :specialty
                            GROUP BY d.DoctorID, d.Name, d.Specialty, dept.Name
                            ORDER BY TotalAppointments DESC
                        """)
                        result = conn.execute(sql, {"specialty": specialty})
                    else:
                        sql = text("""
                            SELECT d.Name AS Doctor, d.Specialty,
                                   dept.Name AS Department,
                                   COUNT(a.AppointmentID) AS TotalAppointments
                            FROM Doctor d
                            JOIN Appointment a ON d.DoctorID = a.DoctorID
                            JOIN Department dept ON d.DepartmentID = dept.DepartmentID
                            GROUP BY d.DoctorID, d.Name, d.Specialty, dept.Name
                            ORDER BY TotalAppointments DESC
                        """)
                        result = conn.execute(sql)
                    columns = list(result.keys())
                    results = [list(row) for row in result.fetchall()]

                # AGGREGATE QUERY 2: Department Patient Load
                elif query_type == 'dept_load':
                    result_title = "Patient Load per Department"
                    sql = text("""
                        SELECT dept.Name AS Department,
                               COUNT(DISTINCT a.PatientID) AS UniquePatients,
                               COUNT(a.AppointmentID) AS TotalAppointments
                        FROM Department dept
                        JOIN Doctor d ON dept.DepartmentID = d.DepartmentID
                        JOIN Appointment a ON d.DoctorID = a.DoctorID
                        GROUP BY dept.DepartmentID, dept.Name
                        ORDER BY UniquePatients DESC
                    """)
                    result = conn.execute(sql)
                    columns = list(result.keys())
                    results = [list(row) for row in result.fetchall()]

        except Exception as e:
            error = str(e)

    return render_template('reports.html', results=results, columns=columns,
                           error=error, result_title=result_title)
'''

if '/reports' not in app_content:
    app_content = app_content.replace("if __name__ == '__main__':", route + "\nif __name__ == '__main__':")
    open(app_path, 'w').write(app_content)
    print("✓ route added to app.py")
else:
    print("✓ route already exists")

print("\nAll done! Restart Flask: python3 app.py")
print("Then open: http://127.0.0.1:5000/reports")
