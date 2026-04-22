# Hospital Management System — SQL Query Examples
**COP 4710: Theory and Structure of Databases — Spring 2026**  
**Team 32 | Florida State University**

---

## How to Run These Queries
1. Start the Flask app: `python3 app.py`
2. Open `http://127.0.0.1:5000/query` in your browser
3. Paste any query below into the text box and click **Run Query**

---

## 1. Basic SELECT Queries

### 1.1 List All Patients
```sql
SELECT * FROM Patient LIMIT 10;
```
**Explanation:** Retrieves all columns from the Patient table. The LIMIT 10 ensures only the first 10 rows are returned so the output is manageable. Useful for quickly verifying patient records exist in the database.

---

### 1.2 List All Doctors
```sql
SELECT * FROM Doctor;
```
**Explanation:** Retrieves all doctor records including their ID, name, phone, license number, specialty, and department assignment. Shows the full doctor catalog in the system.

---

### 1.3 List Available Rooms
```sql
SELECT * FROM Room WHERE Status = 'Available';
```
**Explanation:** Filters the Room table to show only rooms with Available status. Demonstrates a basic WHERE clause filter. Useful for checking room availability before scheduling an appointment.

---

### 1.4 List Scheduled Appointments
```sql
SELECT * FROM Appointment WHERE Status = 'Scheduled';
```
**Explanation:** Retrieves only appointments that are currently in Scheduled status. Demonstrates filtering by an ENUM column value.

---

## 2. JOIN Queries (Multi-Table)

### 2.1 Appointments with Patient, Doctor, and Room Details
```sql
SELECT 
    a.AppointmentID,
    a.Date,
    a.Time,
    a.Status,
    p.Name AS Patient,
    d.Name AS Doctor,
    d.Specialty,
    r.RoomNumber
FROM Appointment a
JOIN Patient p ON a.PatientID = p.PatientID
JOIN Doctor d ON a.DoctorID = d.DoctorID
JOIN Room r ON a.RoomID = r.RoomID
LIMIT 20;
```
**Explanation:** A 4-table JOIN query. Instead of showing foreign key IDs, it joins Patient, Doctor, and Room tables to display human-readable names. Gives a complete picture of each appointment by combining data from four different tables in a single result set.

---

### 2.2 Doctors with Their Department Names
```sql
SELECT 
    d.DoctorID,
    d.Name AS Doctor,
    d.Specialty,
    dept.Name AS Department,
    dept.Location
FROM Doctor d
JOIN Department dept ON d.DepartmentID = dept.DepartmentID;
```
**Explanation:** Joins Doctor and Department tables. Instead of showing the raw DepartmentID foreign key, the query replaces it with the actual department name and location using an INNER JOIN.

---

### 2.3 Medical Records with Patient and Doctor Information
```sql
SELECT 
    mr.RecordID,
    mr.Date,
    mr.Diagnosis,
    mr.Treatment,
    p.Name AS Patient,
    d.Name AS Doctor
FROM MedicalRecord mr
JOIN Appointment a ON mr.AppointmentID = a.AppointmentID
JOIN Patient p ON a.PatientID = p.PatientID
JOIN Doctor d ON a.DoctorID = d.DoctorID
LIMIT 20;
```
**Explanation:** A 4-table JOIN that traces medical records back to the patient and doctor involved. Medical records link to appointments, which link to patients and doctors. This chains those relationships to produce a complete medical record summary.

---

### 2.4 Prescriptions with Medication and Patient Details
```sql
SELECT 
    p.Name AS Patient,
    m.Name AS Medication,
    m.Dosage,
    pr.Instructions,
    mr.Diagnosis
FROM Prescribes pr
JOIN MedicalRecord mr ON pr.RecordID = mr.RecordID
JOIN Medication m ON pr.MedicationID = m.MedicationID
JOIN Appointment a ON mr.AppointmentID = a.AppointmentID
JOIN Patient p ON a.PatientID = p.PatientID
LIMIT 20;
```
**Explanation:** A 5-table JOIN showing which medications were prescribed to which patients, along with dosage and the diagnosis that led to the prescription. Traverses the full chain: Patient → Appointment → MedicalRecord → Prescribes → Medication.

---

## 3. Aggregate Queries (GROUP BY + COUNT)

### 3.1 Total Appointments per Doctor
```sql
SELECT 
    d.Name AS Doctor,
    d.Specialty,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Doctor d
JOIN Appointment a ON d.DoctorID = a.DoctorID
GROUP BY d.DoctorID, d.Name, d.Specialty
ORDER BY TotalAppointments DESC;
```
**Explanation:** Uses COUNT and GROUP BY to calculate how many appointments each doctor has handled. Sorted in descending order so the busiest doctors appear first. Combines JOIN with aggregate functions across two tables.

---

### 3.2 Unique Patients per Department
```sql
SELECT 
    dept.Name AS Department,
    COUNT(DISTINCT a.PatientID) AS UniquePatients
FROM Department dept
JOIN Doctor d ON dept.DepartmentID = d.DepartmentID
JOIN Appointment a ON d.DoctorID = a.DoctorID
GROUP BY dept.DepartmentID, dept.Name
ORDER BY UniquePatients DESC;
```
**Explanation:** Uses COUNT(DISTINCT) to count unique patients per department. The DISTINCT keyword ensures patients with multiple appointments in the same department are counted only once. A 3-table JOIN with aggregate function.

---

### 3.3 Appointments by Status
```sql
SELECT 
    Status,
    COUNT(AppointmentID) AS Total
FROM Appointment
GROUP BY Status;
```
**Explanation:** Groups appointments by status (Scheduled, Completed, Cancelled) and counts each category. Simple aggregate query showing the distribution of appointment outcomes.

---

### 3.4 Most Prescribed Medications
```sql
SELECT 
    m.Name AS Medication,
    m.Dosage,
    COUNT(pr.MedicationID) AS TimesPrescribed
FROM Medication m
JOIN Prescribes pr ON m.MedicationID = pr.MedicationID
GROUP BY m.MedicationID, m.Name, m.Dosage
ORDER BY TimesPrescribed DESC;
```
**Explanation:** Joins Medication and Prescribes tables and counts how many times each medication has been prescribed. Uses COUNT + GROUP BY + ORDER BY to rank medications from most to least prescribed.

---

### 3.5 Doctors with More Than 10 Appointments (HAVING clause)
```sql
SELECT 
    d.Name AS Doctor,
    d.Specialty,
    COUNT(a.AppointmentID) AS Total
FROM Doctor d
JOIN Appointment a ON d.DoctorID = a.DoctorID
GROUP BY d.DoctorID, d.Name, d.Specialty
HAVING COUNT(a.AppointmentID) > 10
ORDER BY Total DESC;
```
**Explanation:** Uses a HAVING clause to filter results after GROUP BY. HAVING works like WHERE but applies to grouped results rather than individual rows. Returns only doctors with more than 10 appointments.

---

## 4. Advanced Queries

### 4.1 Smart Doctor Recommendation (Core Logic)
```sql
SELECT 
    d.DoctorID,
    d.Name,
    d.Specialty,
    dept.Name AS Department,
    d.Phone
FROM Doctor d
JOIN Department dept ON d.DepartmentID = dept.DepartmentID
WHERE d.Specialty = 'Cardiologist'
AND d.DoctorID NOT IN (
    SELECT DoctorID FROM Appointment
    WHERE Date = '2026-04-22'
    AND Time = '10:00:00'
    AND Status = 'Scheduled'
);
```
**Explanation:** The core SQL behind our Smart Doctor Recommendation feature. Finds all doctors matching a specialty who do NOT have a scheduling conflict at the requested date and time. The NOT IN subquery performs conflict detection. Replace 'Cardiologist', the date, and time with desired values.

---

### 4.2 Full Patient History
```sql
SELECT 
    p.Name AS Patient,
    a.Date,
    a.Reason,
    a.Status,
    d.Name AS Doctor,
    mr.Diagnosis,
    mr.Treatment
FROM Patient p
JOIN Appointment a ON p.PatientID = a.PatientID
JOIN Doctor d ON a.DoctorID = d.DoctorID
LEFT JOIN MedicalRecord mr ON a.AppointmentID = mr.AppointmentID
WHERE p.PatientID = 1
ORDER BY a.Date DESC;
```
**Explanation:** Retrieves the complete medical history for a specific patient (change PatientID = 1 to any ID). Uses LEFT JOIN on MedicalRecord so appointments without records still appear. Shows all appointments, doctors seen, and any diagnoses recorded.

---

*Generated for COP 4710 Team 32 — Hospital Management System*  
*GitHub: https://github.com/Dhumo986/hospital-management*
