from enum import Enum
from constants import FeeType

class DoctorFilter:
    def __init__(self, doctors: list):
        self.doctors = doctors

    def filter_by_id(self, doctor_id: int) -> dict:
        """Find a doctor by ID."""
        return next((d for d in self.doctors if d["id"] == doctor_id), None)

    def filter_by_specialization(self, specialization: str) -> list:
        """Filter doctors by specialization."""
        return [d for d in self.doctors if specialization.lower() in d["specialization"].lower()]

    def filter_by_fee(self, max_fee: int) -> list:
        """Filter doctors by fee."""
        return [d for d in self.doctors if d["fee"] <= max_fee]

    def filter_by_experience(self, min_experience: int) -> list:
        """Filter doctors by experience."""
        return [d for d in self.doctors if d["experience_years"] >= min_experience]

    def filter_by_availability(self, is_available: bool) -> list:
        """Filter doctors by availability."""
        return [d for d in self.doctors if d["is_available"] == is_available]

    def filter_by_criteria(self, criteria: dict) -> list:
        """Filter doctors by various criteria."""
        filtered_doctors = self.doctors
        for key, value in criteria.items():
            if key == "id":
                filtered_doctors = [self.filter_by_id(value)]
            elif key == "specialization":
                filtered_doctors = self.filter_by_specialization(value)
            elif key == "fee":
                filtered_doctors = self.filter_by_fee(value)
            elif key == "experience":
                filtered_doctors = self.filter_by_experience(value)
            elif key == "availability":
                filtered_doctors = self.filter_by_availability(value)
        return filtered_doctors

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