from pydantic import BaseModel, Field
from datetime import date

class AppointmentRequest(BaseModel): 
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: date = Field(..., gt=date(1, 1, 1), lt=date.today()) # Changed type to date and added date range validation
    reason: str = Field(..., min_length=5)

class NewDoctor(BaseModel): 
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., ge=1, le=100) # Added maximum value to experience_years field