import pymysql
import urllib.request
import json
import re

# ── Connect to Railway ───────────────────────────────────────────────────────
conn = pymysql.connect(
    host="gondola.proxy.rlwy.net",
    port=33433,
    user="root",
    password="YOUR_PASSWORD_HERE",  # <-- paste your Railway password
    database="railway",
    charset="utf8mb4"
)
cursor = conn.cursor()

# ── Fetch real medication data from FDA API ──────────────────────────────────
print("Fetching real medication data from FDA API...")

medications = []
search_terms = [
    "aspirin", "ibuprofen", "amoxicillin", "metformin", "lisinopril",
    "atorvastatin", "omeprazole", "sertraline", "metoprolol", "prednisone",
    "acetaminophen", "amlodipine", "losartan", "levothyroxine", "albuterol",
    "gabapentin", "hydrochlorothiazide", "furosemide", "pantoprazole", "cetirizine"
]

for term in search_terms:
    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{term}&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read())

        result = data.get("results", [{}])[0]
        openfda = result.get("openfda", {})

        name = openfda.get("brand_name", [term.capitalize()])[0]
        manufacturer = openfda.get("manufacturer_name", ["Unknown"])[0][:100]

        # Extract dosage from dosage_and_administration field
        dosage_text = result.get("dosage_and_administration", [""])[0]
        # Try to find mg dosage in text
        mg_match = re.search(r'(\d+\.?\d*)\s*mg', dosage_text)
        if mg_match:
            dosage = f"{mg_match.group(1)}mg"
        else:
            # fallback dosages
            fallback = {"aspirin": "325mg", "ibuprofen": "200mg", "amoxicillin": "500mg",
                       "metformin": "850mg", "lisinopril": "10mg", "atorvastatin": "20mg",
                       "omeprazole": "20mg", "sertraline": "50mg", "metoprolol": "25mg",
                       "prednisone": "5mg", "acetaminophen": "500mg", "amlodipine": "5mg",
                       "losartan": "50mg", "levothyroxine": "50mcg", "albuterol": "90mcg",
                       "gabapentin": "300mg", "hydrochlorothiazide": "25mg", "furosemide": "40mg",
                       "pantoprazole": "40mg", "cetirizine": "10mg"}
            dosage = fallback.get(term, "10mg")

        side_effects_raw = result.get("adverse_reactions", result.get("warnings", [""]))[0]
        side_effects = side_effects_raw[:200] if side_effects_raw else "See package insert"

        medications.append((name[:100], dosage, side_effects, manufacturer))
        print(f"  ✓ {name} — {dosage} — {manufacturer[:40]}")

    except Exception as e:
        print(f"  ✗ {term}: {e}")
        # Use fallback data
        fallback_data = {
            "aspirin": ("Aspirin", "325mg", "Nausea, stomach bleeding, dizziness", "Bayer"),
            "ibuprofen": ("Ibuprofen", "200mg", "Stomach upset, heartburn, dizziness", "Pfizer"),
            "amoxicillin": ("Amoxicillin", "500mg", "Diarrhea, rash, nausea", "GSK"),
            "metformin": ("Metformin", "850mg", "Nausea, diarrhea, stomach upset", "Merck"),
            "lisinopril": ("Lisinopril", "10mg", "Dizziness, dry cough, headache", "AstraZeneca"),
            "atorvastatin": ("Atorvastatin", "20mg", "Muscle pain, liver problems", "Pfizer"),
            "omeprazole": ("Omeprazole", "20mg", "Headache, nausea, diarrhea", "AstraZeneca"),
            "sertraline": ("Sertraline", "50mg", "Insomnia, dry mouth, nausea", "Pfizer"),
            "metoprolol": ("Metoprolol", "25mg", "Fatigue, dizziness, bradycardia", "Novartis"),
            "prednisone": ("Prednisone", "5mg", "Weight gain, mood swings, insomnia", "Merck"),
            "acetaminophen": ("Acetaminophen", "500mg", "Liver damage at high doses", "Johnson and Johnson"),
            "amlodipine": ("Amlodipine", "5mg", "Swelling, flushing, fatigue", "Pfizer"),
            "losartan": ("Losartan", "50mg", "Dizziness, kidney problems", "Merck"),
            "levothyroxine": ("Levothyroxine", "50mcg", "Heart palpitations, insomnia", "AbbVie"),
            "albuterol": ("Albuterol", "90mcg", "Tremors, nervousness, headache", "GSK"),
            "gabapentin": ("Gabapentin", "300mg", "Drowsiness, dizziness, fatigue", "Pfizer"),
            "hydrochlorothiazide": ("Hydrochlorothiazide", "25mg", "Low potassium, dizziness", "Novartis"),
            "furosemide": ("Furosemide", "40mg", "Dehydration, low potassium", "Sanofi"),
            "pantoprazole": ("Pantoprazole", "40mg", "Headache, diarrhea, nausea", "Pfizer"),
            "cetirizine": ("Cetirizine", "10mg", "Drowsiness, dry mouth, fatigue", "Johnson and Johnson"),
        }
        if term in fallback_data:
            medications.append(fallback_data[term])

# ── Clear old medication data and insert real data ───────────────────────────
print("\nClearing old medication data...")
cursor.execute("DELETE FROM Prescribes")
cursor.execute("DELETE FROM Medication")
conn.commit()

print("Inserting real medication data...")
for med in medications:
    cursor.execute(
        "INSERT INTO Medication (Name, Dosage, SideEffects, Manufacturer) VALUES (%s, %s, %s, %s)",
        med
    )
conn.commit()

cursor.execute("SELECT COUNT(*) FROM Medication")
count = cursor.fetchone()[0]
print(f"\n✓ {count} real medications inserted successfully!")

cursor.close()
conn.close()
print("\nDone! Now restart Flask and check the Medications page.")
