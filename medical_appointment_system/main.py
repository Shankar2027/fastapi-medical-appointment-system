from fastapi import FastAPI, HTTPException, Query, status
import database
from models import AppointmentRequest, NewDoctor
from helpers import find_doctor, calculate_fee, filter_doctors_logic
from typing import Optional, List
from constants import MAX_DOCTORS_PER_PAGE, MAX_APPOINTMENTS_PER_PAGE
from pydantic import BaseModel
from typing import Any

# Define a constant for the magic number
UNIQUE_DOCTOR_ERROR_CODE = 400

class DoctorDAO:
    def get_all_doctors(self):
        return database.doctors

    def get_doctor_by_id(self, doctor_id: int):
        return find_doctor(doctor_id)

    def add_doctor(self, doc: NewDoctor):
        if any(d["name"] == doc.name for d in database.doctors): 
            raise HTTPException(UNIQUE_DOCTOR_ERROR_CODE, "Doctor with this name already exists")
        new_d = {"id": len(database.doctors) + 1, **doc.model_dump()}
        database.doctors.append(new_d)
        return new_d

    def _update_doctor(self, doctor_id: int, fee: int = None, is_available: bool = None):
        doc = find_doctor(doctor_id)
        if not doc: 
            raise HTTPException(404, "Doctor not found")
        if fee is not None: 
            doc["fee"] = fee
        if is_available is not None: 
            doc["is_available"] = is_available
        return doc

    def update_doctor(self, doctor_id: int, fee: int = None, is_available: bool = None):
        return self._update_doctor(doctor_id, fee, is_available)

    def delete_doctor(self, doctor_id: int):
        doc = find_doctor(doctor_id)
        if not doc: 
            raise HTTPException(404, "Doctor not found")
        # Check if doctor has active appointments
        if any(a["doc_id"] == doctor_id and a["status"] in ["scheduled", "confirmed"] for a in database.appointments):
            raise HTTPException(400, "Cannot delete doctor with active or scheduled appointments")
        database.doctors.remove(doc)
        return {"message": "Doctor deleted successfully"}

class AppointmentDAO:
    def get_all_appointments(self):
        return database.appointments

    def get_active_appointments(self):
        return [a for a in database.appointments if a["status"] in ["scheduled", "confirmed"]]

    def search_appointments(self, patient_name: str):
        results = []
        for a in database.appointments:
            if patient_name.lower() in a["patient"].lower():
                results.append(a)
        return {"results": results, "total": len(results)}

    def get_appointments_by_doctor(self, doctor_id: int):
        return [a for a in database.appointments if a["doc_id"] == doctor_id]

    def create_appointment(self, req: AppointmentRequest):
        doc = find_doctor(req.doctor_id)
        if not doc or not doc["is_available"]: 
            raise HTTPException(400, "Doctor unavailable or not found")
        fee = calculate_fee(doc["fee"], req.appointment_type, req.senior_citizen)
        new_appt = {
            "id": len(database.appointments) + 1, 
            "patient": req.patient_name, 
            "doctor": doc["name"], 
            "fee": fee, 
            "status": "scheduled", 
            "doc_id": doc["id"]
        }
        database.appointments.append(new_appt)
        return new_appt

    def confirm_appointment(self, id: int):
        for a in database.appointments:
            if a["id"] == id: 
                a["status"] = "confirmed"
                return a
        raise HTTPException(404, "Appointment not found")

    def cancel_appointment(self, id: int):
        for a in database.appointments:
            if a["id"] == id:
                a["status"] = "cancelled"
                doc = find_doctor(a["doc_id"])
                if doc: doc["is_available"] = True
                return a
        raise HTTPException(404, "Appointment not found")

    def complete_appointment(self, id: int):
        for a in database.appointments:
            if a["id"] == id:
                a["status"] = "completed"
                return a
        raise HTTPException(404)

doctor_dao = DoctorDAO()
appointment_dao = AppointmentDAO()

@app.get("/doctors/summary")
def get_summary():
    most_exp = max(database.doctors, key=lambda x: x['experience_years'])
    cheapest = min(database.doctors, key=lambda x: x['fee'])
    specs = {s: len([d for d in database.doctors if d['specialization'] == s]) for s in set(d['specialization'] for d in database.doctors)}
    return {
        "total": len(database.doctors), 
        "available": len([d for d in database.doctors if d['is_available']]), 
        "most_experienced": most_exp['name'], 
        "cheapest_fee": cheapest['fee'], 
        "breakdown": specs
    }

@app.get("/doctors/filter")
def filter_docs(specialization: str = None, max_fee: int = None, min_experience: int = None, is_available: bool = None):
    return filter_doctors_logic(specialization, max_fee, min_experience, is_available)

@app.get("/doctors/search")
def search_docs(keyword: str):
    results = []
    for d in database.doctors:
        if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower():
            results.append(d)
    if not results: 
        return {"message": f"No doctors found matching '{keyword}'"}
    return {"results": results, "total_found": len(results)}

@app.get("/doctors/sort")
def sort_docs(sort_by: str = "fee", order: str = "asc"):
    if sort_by not in ["fee", "name", "experience_years"]: 
        raise HTTPException(400, "Invalid sort field")
    rev = (order == "desc")
    sorted_list = sorted(database.doctors, key=lambda x: x[sort_by], reverse=rev)
    return {"sorted_data": sorted_list, "metadata": {"sort_by": sort_by, "order": order}}

@app.get("/doctors/page")
def paginate_docs(page: int = 1):
    start = (page - 1) * MAX_DOCTORS_PER_PAGE
    end = start + MAX_DOCTORS_PER_PAGE
    return {"data": database.doctors[start:end], "total_pages": 1, "current_page": page}

@app.get("/doctors/browse")
def browse_doctors(keyword: str = None, sort_by: str = "fee", order: str = "asc", page: int = 1):
    data = database.doctors
    if keyword: 
        data = [d for d in data if keyword.lower() in d["name"].lower()]
    rev = (order == "desc")
    data = sorted(data, key=lambda x: x.get(sort_by, "fee"), reverse=rev)
    start = (page - 1) * MAX_DOCTORS_PER_PAGE
    return {"results": data[start:start+MAX_DOCTORS_PER_PAGE], "page": page}

# --- APPOINTMENT ROUTES ---
@app.get("/appointments/active")
def get_active_appts():
    return appointment_dao.get_active_appointments()

@app.get("/appointments/search")
def search_appointments(patient_name: str):
    return appointment_dao.search_appointments(patient_name)

@app.get("/appointments/by-doctor/{doctor_id}")
def get_appts_by_doctor(doctor_id: int):
    return appointment_dao.get_appointments_by_doctor(doctor_id)

@app.get("/appointments")
def get_all_appointments():
    return {"appointments": database.appointments, "total": len(database.appointments)}

@app.post("/appointments", status_code=201)
def create_appt(req: AppointmentRequest):
    return appointment_dao.create_appointment(req)

@app.post("/appointments/{id}/confirm")
def confirm_appt(id: int):
    return appointment_dao.confirm_appointment(id)

@app.post("/appointments/{id}/cancel")
def cancel_appt(id: int):
    return appointment_dao.cancel_appointment(id)

@app.post("/appointments/{id}/complete")
def complete_appt(id: int):
    return appointment_dao.complete_appointment(id)

# --- DOCTOR CRUD (Variable Routes) ---
@app.get("/doctors")
def get_all_docs():
    return {"doctors": database.doctors, "total": len(database.doctors), "available_count": len([d for d in database.doctors if d['is_available']])}

@app.get("/doctors/{doctor_id}")
def get_doc(doctor_id: int):
    return doctor_dao.get_doctor_by_id(doctor_id)

@app.post("/doctors", status_code=201)
def add_doc(doc: NewDoctor):
    return doctor_dao.add_doctor(doc)

@app.put("/doctors/{doctor_id}")
def update_doc(doctor_id: int, fee: int = None, is_available: bool = None):
    return doctor_dao.update_doctor(doctor_id, fee, is_available)

@app.delete("/doctors/{doctor_id}")
def delete_doc(doctor_id: int):
    return doctor_dao.delete_doctor(doctor_id)