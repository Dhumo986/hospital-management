import os

# Add dosage filter card to reports.html
reports_path = '/Users/dhruvupadhyay/hospital-management/templates/reports.html'
content = open(reports_path).read()

dosage_card = '''
<!-- DOSAGE FILTER SECTION -->
<div class="card" style="margin-bottom:24px">
  <div class="card-header">
    <h2>💊 Medication Dosage Filter</h2>
  </div>
  <div class="card-body">
    <p style="color:var(--text-muted);margin-bottom:20px;font-size:13.5px">
      Use the arrows to filter medications by dosage amount. Shows aggregate count of medications at each dosage level.
    </p>
    <form method="POST" action="/reports" id="dosageForm">
      <input type="hidden" name="query_type" value="dosage_filter"/>
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:20px">
        <div>
          <label style="font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;display:block;margin-bottom:6px">Sort Dosage</label>
          <div style="display:flex;gap:8px">
            <button type="submit" name="dosage_order" value="asc" class="btn btn-outline" style="font-size:18px;padding:8px 16px" title="Lowest to Highest">
              ↑ Low to High
            </button>
            <button type="submit" name="dosage_order" value="desc" class="btn btn-outline" style="font-size:18px;padding:8px 16px" title="Highest to Lowest">
              ↓ High to Low
            </button>
          </div>
        </div>
        <div>
          <label style="font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;display:block;margin-bottom:6px">Filter by Manufacturer</label>
          <select name="manufacturer" onchange="document.getElementById(\'dosageForm\').submit()" style="padding:9px 12px;border:1px solid var(--border);border-radius:7px;font-size:13.5px">
            <option value="">All Manufacturers</option>
            <option>Pfizer</option>
            <option>Merck</option>
            <option>AstraZeneca</option>
            <option>GSK</option>
            <option>Novartis</option>
            <option>Bayer</option>
            <option>Sanofi</option>
            <option>AbbVie</option>
            <option>Johnson and Johnson</option>
          </select>
        </div>
      </div>
    </form>
  </div>
</div>

'''

# Insert before the results section
old = '<!-- RESULTS -->'
new = dosage_card + '<!-- RESULTS -->'
if 'dosage_filter' not in content:
    content = content.replace(old, new)
    open(reports_path, 'w').write(content)
    print("✓ Dosage filter added to reports.html")
else:
    print("✓ Already exists")

# Add dosage route to app.py
app_path = '/Users/dhruvupadhyay/hospital-management/app.py'
app_content = open(app_path).read()

dosage_route = '''
                # DOSAGE FILTER QUERY
                elif query_type == 'dosage_filter':
                    order = request.form.get('dosage_order', 'asc')
                    manufacturer = request.form.get('manufacturer', '')
                    result_title = f"Medications sorted by Dosage ({'Low to High' if order == 'asc' else 'High to Low'})"
                    if manufacturer:
                        sql = text("""
                            SELECT Name, Dosage, Manufacturer, SideEffects,
                                   CAST(REGEXP_REPLACE(Dosage, '[^0-9.]', '') AS DECIMAL(10,2)) AS DosageNum
                            FROM Medication
                            WHERE Manufacturer = :manufacturer
                            ORDER BY DosageNum """ + ("ASC" if order == "asc" else "DESC"))
                        result = conn.execute(sql, {"manufacturer": manufacturer})
                    else:
                        sql = text("""
                            SELECT Name, Dosage, Manufacturer, SideEffects,
                                   CAST(REGEXP_REPLACE(Dosage, '[^0-9.]', '') AS DECIMAL(10,2)) AS DosageNum
                            FROM Medication
                            ORDER BY DosageNum """ + ("ASC" if order == "asc" else "DESC"))
                        result = conn.execute(sql)
                    columns = list(result.keys())
                    results = [list(row) for row in result.fetchall()]
'''

if 'dosage_filter' not in app_content:
    app_content = app_content.replace(
        "        except Exception as e:\n            error = str(e)",
        dosage_route + "\n        except Exception as e:\n            error = str(e)"
    )
    open(app_path, 'w').write(app_content)
    print("✓ Dosage route added to app.py")
else:
    print("✓ Route already exists")

print("\nDone! Now restart Flask: python3 app.py")
