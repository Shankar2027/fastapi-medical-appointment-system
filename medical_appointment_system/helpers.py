from database import doctors
from exceptions import DoctorNotFoundException, ValueError

def find_doctor(doctor_id: int):
    try:
        return next((d for d in doctors if d["id"] == doctor_id), None)
    except StopIteration:
        raise DoctorNotFoundException(f"Doctor with ID {doctor_id} not found")

def calculate_fee(base_fee: int, appt_type: str, is_senior: bool):
    if not isinstance(base_fee, (int, float)) or base_fee <= 0:
        raise ValueError("Base fee must be a positive number")
    if appt_type not in ["video", "emergency"]:
        raise ValueError("Invalid appointment type")
    if not isinstance(is_senior, bool):
        raise ValueError("Is senior must be a boolean value")
    fee = float(base_fee)
    if appt_type == "video": fee *= 0.8
    elif appt_type == "emergency": fee *= 1.5
    if is_senior: fee *= 0.85
    return round(fee, 2)

def filter_doctors_logic(spec: str = None, max_f: int = None, min_exp: int = None, avail: bool = None):
    filters = {
        "spec": spec,
        "max_f": max_f,
        "min_exp": min_exp,
        "avail": avail
    }
    filtered_doctors = doctors.copy()
    for key, value in filters.items():
        if value is not None:
            if key == "spec":
                filtered_doctors = [d for d in filtered_doctors if value.lower() in d["specialization"].lower()]
            elif key == "max_f":
                filtered_doctors = [d for d in filtered_doctors if d["fee"] <= value]
            elif key == "min_exp":
                filtered_doctors = [d for d in filtered_doctors if d["experience_years"] >= value]
            elif key == "avail":
                filtered_doctors = [d for d in filtered_doctors if d["is_available"] == value]
    return filtered_doctors