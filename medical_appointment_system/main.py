from fastapi import FastAPI, HTTPException, Query, status
import math
import database
from models import AppointmentRequest, NewDoctor
from helpers import find_doctor, calculate_fee, filter_doctors_logic
from typing import Optional, List

app = FastAPI(title="MediCare Clinic Final Project")

# --- Q1: HOME ---
@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}

# --- FIXED DOCTOR ROUTES ---

@app.get("/doctors/summary") # Q5
def get_summary():
    all_d = database.doctors
    most_exp = max(all_d, key=lambda x: x['experience_years'])
    cheapest = min(all_d, key=lambda x: x['fee'])
    specs = {s: len([d for d in all_d if d['specialization'] == s]) for s in set(d['specialization'] for d in all_d)}
    return {
        "total": len(all_d), 
        "available": len([d for d in all_d if d['is_available']]), 
        "most_experienced": most_exp['name'], 
        "cheapest_fee": cheapest['fee'], 
        "breakdown": specs
    }


@app.get("/doctors/filter") # Q10
def filter_docs(specialization: str = None, max_fee: int = None, min_experience: int = None, is_available: bool = None):
    return filter_doctors_logic(specialization, max_fee, min_experience, is_available)


@app.get("/doctors/search") # Q16
def search_docs(keyword: str):
    results = [d for d in database.doctors if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    if not results: 
        return {"message": f"No doctors found matching '{keyword}'"}
    return {"results": results, "total_found": len(results)}


@app.get("/doctors/sort") # Q17
def sort_docs(sort_by: str = "fee", order: str = "asc"):
    if sort_by not in ["fee", "name", "experience_years"]: 
        raise HTTPException(400, "Invalid sort field")
    rev = (order == "desc")
    sorted_list = sorted(database.doctors, key=lambda x: x[sort_by], reverse=rev)
    return {"sorted_data": sorted_list, "metadata": {"sort_by": sort_by, "order": order}}


@app.get("/doctors/page") # Q18
def paginate_docs(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit
    total_pages = math.ceil(len(database.doctors) / limit)
    return {"data": database.doctors[start:end], "total_pages": total_pages, "current_page": page}


@app.get("/doctors/browse") # Q20 (Combined)
def browse_doctors(keyword: str = None, sort_by: str = "fee", order: str = "asc", page: int = 1, limit: int = 4):
    data = database.doctors
    if keyword: 
        data = [d for d in data if keyword.lower() in d["name"].lower()]
    rev = (order == "desc")
    data = sorted(data, key=lambda x: x.get(sort_by, "fee"), reverse=rev)
    start = (page - 1) * limit
    return {"results": data[start:start+limit], "page": page, "limit": limit}


# --- APPOINTMENT ROUTES ---

@app.get("/appointments/active") # Q15
def get_active_appts():
    return [a for a in database.appointments if a["status"] in ["scheduled", "confirmed"]]


@app.get("/appointments/search") # Q19
def search_appointments(patient_name: str):
    results = [a for a in database.appointments if patient_name.lower() in a["patient"].lower()]
    return {"results": results, "total": len(results)}


@app.get("/appointments/by-doctor/{doctor_id}") # Q15
def get_appts_by_doctor(doctor_id: int):
    return [a for a in database.appointments if a["doc_id"] == doctor_id]


@app.get("/appointments") # Q4
def get_all_appointments():
    return {"appointments": database.appointments, "total": len(database.appointments)}


@app.post("/appointments", status_code=201) # Q8 & Q9
def create_appt(req: AppointmentRequest):
    doc = find_doctor(req.doctor_id)
    if not doc or not doc["is_available"]: 
        raise HTTPException(400, "Doctor unavailable or not found")
    fee = calculate_fee(doc["fee"], req.appointment_type, req.senior_citizen)
    new_appt = {
        "id": database.appt_counter, 
        "patient": req.patient_name, 
        "doctor": doc["name"], 
        "fee": fee, 
        "status": "scheduled", 
        "doc_id": doc["id"]
    }
    database.appointments.append(new_appt)
    database.appt_counter += 1
    return new_appt


@app.post("/appointments/{id}/confirm") # Q14
def confirm_appt(id: int):
    for a in database.appointments:
        if a["id"] == id: 
            a["status"] = "confirmed"
            return a
    raise HTTPException(404, "Appointment not found")


@app.post("/appointments/{id}/cancel") # Q14
def cancel_appt(id: int):
    for a in database.appointments:
        if a["id"] == id:
            a["status"] = "cancelled"
            doc = find_doctor(a["doc_id"])
            if doc: doc["is_available"] = True
            return a
    raise HTTPException(404, "Appointment not found")


@app.post("/appointments/{id}/complete") # Q15
def complete_appt(id: int):
    for a in database.appointments:
        if a["id"] == id:
            a["status"] = "completed"
            return a
    raise HTTPException(404)


# --- DOCTOR CRUD (Variable Routes) ---

@app.get("/doctors") # Q2
def get_all_docs():
    return {"doctors": database.doctors, "total": len(database.doctors), "available_count": len([d for d in database.doctors if d['is_available']])}


@app.get("/doctors/{doctor_id}") # Q3
def get_doc(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc: 
        raise HTTPException(404, "Not found")
    return doc


@app.post("/doctors", status_code=201) # Q11
def add_doctor(doc: NewDoctor):
    if any(d["name"] == doc.name for d in database.doctors): 
        raise HTTPException(400, "Doctor with this name already exists")
    new_d = {"id": len(database.doctors) + 1, **doc.model_dump()}
    database.doctors.append(new_d)
    return new_d


# FIX for Q12: Removing explicit Optional to avoid Pydantic build error
@app.put("/doctors/{doctor_id}") 
def update_doc(doctor_id: int, fee: int = None, is_available: bool = None):
    doc = find_doctor(doctor_id)
    if not doc: 
        raise HTTPException(404, "Doctor not found")
    if fee is not None: 
        doc["fee"] = fee
    if is_available is not None: 
        doc["is_available"] = is_available
    return doc


@app.delete("/doctors/{doctor_id}") # Q13
def delete_doc(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc: 
        raise HTTPException(404, "Doctor not found")
    # Check if doctor has active appointments
    if any(a["doc_id"] == doctor_id and a["status"] in ["scheduled", "confirmed"] for a in database.appointments):
        raise HTTPException(400, "Cannot delete doctor with active or scheduled appointments")
    database.doctors.remove(doc)
    return {"message": "Doctor deleted successfully"}