from enum import Enum
from constants import FeeType

def find_doctor(doctors: list, doctor_id: int) -> dict:
    """Find a doctor by ID."""
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(base_fee: int, appointment_type: str, is_senior: bool) -> float:
    """Calculate the fee for an appointment."""
    fee = base_fee
    if appointment_type == "video":
        fee *= FeeType.VIDEO_DISCOUNT_FEE.value
    elif appointment_type == "emergency":
        fee *= FeeType.EMERGENCY_SURCHARGE_FEE.value
    if is_senior:
        fee *= FeeType.SENIOR_DISCOUNT_FEE.value
    return round(fee, 2)

def filter_doctors_by_specialization(doctors: list, specialization: str) -> list:
    """Filter doctors by specialization."""
    return [d for d in doctors if specialization.lower() in d["specialization"].lower()]

def filter_doctors_by_fee(doctors: list, max_fee: int) -> list:
    """Filter doctors by fee."""
    return [d for d in doctors if d["fee"] <= max_fee]

def filter_doctors_by_experience(doctors: list, min_experience: int) -> list:
    """Filter doctors by experience."""
    return [d for d in doctors if d["experience_years"] >= min_experience]

def filter_doctors_by_availability(doctors: list, is_available: bool) -> list:
    """Filter doctors by availability."""
    return [d for d in doctors if d["is_available"] == is_available]

def filter_doctors_by_specialization_and_fee(doctors: list, spec: str, max_f: int) -> list:
    """Filter doctors by specialization and fee."""
    return filter_doctors_by_fee(filter_doctors_by_specialization(doctors, spec), max_f)

def filter_doctors_by_specialization_and_experience(doctors: list, spec: str, min_exp: int) -> list:
    """Filter doctors by specialization and experience."""
    return filter_doctors_by_experience(filter_doctors_by_specialization(doctors, spec), min_exp)

def filter_doctors_by_specialization_and_availability(doctors: list, spec: str, avail: bool) -> list:
    """Filter doctors by specialization and availability."""
    return filter_doctors_by_availability(filter_doctors_by_specialization(doctors, spec), avail)

def filter_doctors_by_fee_and_experience(doctors: list, max_f: int, min_exp: int) -> list:
    """Filter doctors by fee and experience."""
    return filter_doctors_by_experience(filter_doctors_by_fee(doctors, max_f), min_exp)

def filter_doctors_by_fee_and_availability(doctors: list, max_f: int, avail: bool) -> list:
    """Filter doctors by fee and availability."""
    return filter_doctors_by_availability(filter_doctors_by_fee(doctors, max_f), avail)

def filter_doctors_by_experience_and_availability(doctors: list, min_exp: int, avail: bool) -> list:
    """Filter doctors by experience and availability."""
    return filter_doctors_by_availability(filter_doctors_by_experience(doctors, min_exp), avail)

def filter_doctors_logic(doctors: list, spec: str = None, max_f: int = None, min_exp: int = None, avail: bool = None) -> list:
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