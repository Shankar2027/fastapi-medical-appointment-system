from typing import Optional
from datetime import datetime

class AppointmentRequest(BaseModel): 
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: datetime = Field(..., min_items=8)
    reason: str = Field(..., min_length=5)
    appointment_type: Optional[str] = None
    senior_citizen: bool = False 

class NewDoctor(BaseModel): 
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)