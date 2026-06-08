from typing import List

# Define named constants for magic numbers
VIDEO_DISCOUNT_FEE = 0.8
EMERGENCY_SURCHARGE_FEE = 1.5
SENIOR_DISCOUNT_FEE = 0.85

def find_doctor(doctor_id: int) -> dict:
    """Find a doctor by ID."""
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(base_fee: int, appointment_type: str, is_senior: bool) -> float:
    """Calculate the fee for an appointment."""
    fee = base_fee
    if appointment_type == "video":
        fee *= VIDEO_DISCOUNT_FEE
    elif appointment_type == "emergency":
        fee *= EMERGENCY_SURCHARGE_FEE
    if is_senior:
        fee *= SENIOR_DISCOUNT_FEE
    return round(fee, 2)

def filter_doctors_by_specialization(doctors: List[dict], specialization: str) -> List[dict]:
    """Filter doctors by specialization."""
    return [d for d in doctors if specialization.lower() in d["specialization"].lower()]

def filter_doctors_by_fee(doctors: List[dict], max_fee: int) -> List[dict]:
    """Filter doctors by fee."""
    return [d for d in doctors if d["fee"] <= max_fee]

def filter_doctors_by_experience(doctors: List[dict], min_experience: int) -> List[dict]:
    """Filter doctors by experience."""
    return [d for d in doctors if d["experience_years"] >= min_experience]

def filter_doctors_by_availability(doctors: List[dict], is_available: bool) -> List[dict]:
    """Filter doctors by availability."""
    return [d for d in doctors if d["is_available"] == is_available]

def filter_doctors_logic(doctors: List[dict], spec: str = None, max_f: int = None, min_exp: int = None, avail: bool = None) -> List[dict]:
    """Filter doctors based on various criteria."""
    filtered_doctors = doctors
    if spec is not None:
        filtered_doctors = filter_doctors_by_specialization(filtered_doctors, spec)
    if max_f is not None:
        filtered_doctors = filter_doctors_by_fee(filtered_doctors, max_f)
    if min_exp is not None:
        filtered_doctors = filter_doctors_by_experience(filtered_doctors, min_exp)
    if avail is not None:
        filtered_doctors = filter_doctors_by_availability(filtered_doctors, avail)
    return filtered_doctors