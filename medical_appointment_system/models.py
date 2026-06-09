from typing import get_type_hints

class AppointmentRequest(BaseModel): 
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: datetime = Field(..., min_value=8)
    reason: str = Field(..., min_length=5)

class NewDoctor(BaseModel): 
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., ge=1)