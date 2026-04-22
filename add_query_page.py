import os

# 1. Add query template
query_template = '''{% extends "base.html" %}
{% block title %}SQL Query{% endblock %}
{% block page_title %}SQL Query Runner{% endblock %}

{% block content %}
<div class="card" style="margin-bottom:24px">
  <div class="card-header"><h2>🔍 Run SQL Query</h2></div>
  <div class="card-body">
    <p style="color:var(--text-muted);margin-bottom:16px;font-size:13.5px">
      Only SELECT queries are allowed. Examples: <code>SELECT * FROM Patient LIMIT 10</code> or <code>SELECT * FROM Doctor</code>
    </p>
    <form method="POST" action="/query">
      <div class="form-group full" style="margin-bottom:16px">
        <label>SQL Query</label>
        <textarea name="query" rows="4" placeholder="SELECT * FROM Patient LIMIT 10" style="font-family:\'DM Mono\',monospace;font-size:13px">{{ query or "" }}</textarea>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px">
        <button type="submit" class="btn btn-primary">▶ Run Query</button>
        <a href="/query" class="btn btn-outline">Clear</a>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
        <span style="font-size:11px;color:var(--text-muted);font-weight:600;margin-right:4px">QUICK QUERIES:</span>
        {% for label, q in quick_queries %}
        <button type="submit" name="query" value="{{ q }}" class="btn btn-sm btn-outline" style="font-size:11px">{{ label }}</button>
        {% endfor %}
      </div>
    </form>
  </div>
</div>

{% if error %}
<div class="alert alert-danger">{{ error }}</div>
{% endif %}

{% if results is not none %}
<div class="card">
  <div class="card-header">
    <h2>Results {% if results %}({{ results|length }} rows){% endif %}</h2>
  </div>
  {% if results %}
  <div class="table-wrap"><table>
    <thead><tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr></thead>
    <tbody>
    {% for row in results %}
    <tr>{% for cell in row %}<td>{{ cell if cell is not none else "NULL" }}</td>{% endfor %}</tr>
    {% endfor %}
    </tbody>
  </table></div>
  {% else %}
  <div class="card-body" style="color:var(--text-muted);text-align:center;padding:32px">No results returned.</div>
  {% endif %}
</div>
{% endif %}
{% endblock %}'''

with open('/Users/dhruvupadhyay/hospital-management/templates/query.html', 'w') as f:
    f.write(query_template)
print("✓ query.html created")

# 2. Add sidebar link to base.html
base_path = '/Users/dhruvupadhyay/hospital-management/templates/base.html'
content = open(base_path).read()
old = '  </nav>'
new = '    <a href="/query"><span class="icon">🔍</span> SQL Query</a>\n  </nav>'
if '/query' not in content:
    content = content.replace(old, new)
    open(base_path, 'w').write(content)
    print("✓ sidebar link added")
else:
    print("✓ sidebar link already exists")

# 3. Add route to app.py
app_path = '/Users/dhruvupadhyay/hospital-management/app.py'
app_content = open(app_path).read()

route = '''
# ══════════════════════════════════════════════════════════════════════════════
# SQL QUERY RUNNER
# ══════════════════════════════════════════════════════════════════════════════
@app.route('/query', methods=['GET', 'POST'])
def query_runner():
    results = None
    columns = []
    error = None
    query = None

    quick_queries = [
        ("All Patients", "SELECT * FROM Patient LIMIT 20"),
        ("All Doctors", "SELECT * FROM Doctor LIMIT 20"),
        ("All Appointments", "SELECT AppointmentID, Date, Time, Status, PatientID, DoctorID FROM Appointment LIMIT 20"),
        ("Appointments + Patient + Doctor", "SELECT a.AppointmentID, a.Date, a.Time, a.Status, p.Name AS Patient, d.Name AS Doctor, r.RoomNumber FROM Appointment a JOIN Patient p ON a.PatientID=p.PatientID JOIN Doctor d ON a.DoctorID=d.DoctorID JOIN Room r ON a.RoomID=r.RoomID LIMIT 20"),
        ("Appointments per Doctor", "SELECT d.Name, d.Specialty, COUNT(a.AppointmentID) AS Total FROM Doctor d JOIN Appointment a ON d.DoctorID=a.DoctorID GROUP BY d.DoctorID ORDER BY Total DESC"),
        ("Patients per Department", "SELECT dept.Name, COUNT(DISTINCT a.PatientID) AS Patients FROM Department dept JOIN Doctor d ON dept.DepartmentID=d.DepartmentID JOIN Appointment a ON d.DoctorID=a.DoctorID GROUP BY dept.DepartmentID ORDER BY Patients DESC"),
        ("Top Medications", "SELECT m.Name, COUNT(p.MedicationID) AS Prescribed FROM Medication m JOIN Prescribes p ON m.MedicationID=p.MedicationID GROUP BY m.MedicationID ORDER BY Prescribed DESC"),
        ("All Departments", "SELECT * FROM Department"),
        ("All Medications", "SELECT * FROM Medication"),
        ("All Rooms", "SELECT * FROM Room"),
    ]

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            if not query.lower().startswith('select'):
                error = "Only SELECT queries are allowed."
            else:
                try:
                    from sqlalchemy import text
                    with db.engine.connect() as conn:
                        result = conn.execute(text(query))
                        columns = list(result.keys())
                        results = [list(row) for row in result.fetchall()]
                except Exception as e:
                    error = f"Query error: {str(e)}"

    return render_template('query.html', results=results, columns=columns, error=error, query=query, quick_queries=quick_queries)
'''

if '/query' not in app_content:
    # Insert before if __name__
    app_content = app_content.replace("if __name__ == '__main__':", route + "\nif __name__ == '__main__':")
    open(app_path, 'w').write(app_content)
    print("✓ route added to app.py")
else:
    print("✓ route already exists")

print("\nAll done! Restart Flask with: python3 app.py")
