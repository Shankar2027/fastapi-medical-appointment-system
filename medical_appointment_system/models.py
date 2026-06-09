from pydantic import BaseModel, Field

MIN_NAME_LENGTH = 2
MIN_REASON_LENGTH = 5
MIN_EXPERIENCE_YEARS = 1
MAX_EXPERIENCE_YEARS = 100

class AppointmentRequest(BaseModel): 
    patient_name: str = Field(..., min_length=MIN_NAME_LENGTH)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., gt="2022-01-01", lt="2024-12-31") # Changed type to str and added date range validation
    reason: str = Field(..., min_length=MIN_REASON_LENGTH)

class NewDoctor(BaseModel): 
    name: str = Field(..., min_length=MIN_NAME_LENGTH)
    specialization: str = Field(..., min_length=MIN_NAME_LENGTH)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., ge=MIN_EXPERIENCE_YEARS, le=MAX_EXPERIENCE_YEARS)