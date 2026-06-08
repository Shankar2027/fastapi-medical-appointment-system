from database import doctors

# Define named constants for magic numbers
FEE_VIDEO_DISCOUNT = 0.8
FEE_EMERGENCY_SURCHARGE = 1.5
FEE_SENIOR_DISCOUNT = 0.85

def find_doctor(doctor_id: int): # Q7
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(base_fee: int, appt_type: str, is_senior: bool): # Q7 & Q9
    fee = base_fee
    if appt_type == "video": fee *= FEE_VIDEO_DISCOUNT
    elif appt_type == "emergency": fee *= FEE_EMERGENCY_SURCHARGE
    if is_senior: fee *= FEE_SENIOR_DISCOUNT
    return round(fee, 2)

def filter_doctors_logic(spec: str = None, max_f: int = None, min_exp: int = None, avail: bool = None): # Q10
    filtered = doctors
    if spec is not None: filtered = [d for d in filtered if spec.lower() in d["specialization"].lower()]
    if max_f is not None: filtered = [d for d in filtered if d["fee"] <= max_f]
    if min_exp is not None: filtered = [d for d in filtered if d["experience_years"] >= min_exp]
    if avail is not None: filtered = [d for d in filtered if d["is_available"] == avail]
    return filtered