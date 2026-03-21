from pydantic import BaseModel, Field
from typing import Optional

class AppointmentRequest(BaseModel): # Q6
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False # Q9

class NewDoctor(BaseModel): # Q11
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True