# database.py

# Define named constants
START_DATE = '2022-01-01'
NUMBER_OF_APPOINTMENTS = 6

# Define doctor's fee and experience years
DOCTOR_FEE_RANGES = [
    {"fee": 200, "experience_years": 12, "is_available": True},
    {"fee": 300, "experience_years": 8, "is_available": False},
    {"fee": 350, "experience_years": 3, "is_available": True},
    {"fee": 400, "experience_years": 5, "is_available": True},
    {"fee": 500, "experience_years": 10, "is_available": True},
    {"fee": 600, "experience_years": 15, "is_available": True},
]

# Define doctors
doctors = [
    {
        "id": 1, 
        "name": "Dr. Mounika", 
        "specialization": "Cardiologist", 
        "fee": DOCTOR_FEE_RANGES[0]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[0]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[0]["is_available"]
    },
    {
        "id": 2, 
        "name": "Dr. Shankar", 
        "specialization": "Dermatologist", 
        "fee": DOCTOR_FEE_RANGES[1]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[1]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[1]["is_available"]
    },
    {
        "id": 3, 
        "name": "Dr. Mahitha", 
        "specialization": "Pediatrician", 
        "fee": DOCTOR_FEE_RANGES[2]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[2]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[2]["is_available"]
    },
    {
        "id": 4, 
        "name": "Dr. Spoorthi", 
        "specialization": "General", 
        "fee": DOCTOR_FEE_RANGES[3]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[3]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[3]["is_available"]
    },
    {
        "id": 5, 
        "name": "Dr. Yashwanth", 
        "specialization": "Cardiologist", 
        "fee": DOCTOR_FEE_RANGES[4]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[4]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[4]["is_available"]
    },
    {
        "id": 6, 
        "name": "Dr. Keerthi", 
        "specialization": "Pediatrician", 
        "fee": DOCTOR_FEE_RANGES[5]["fee"], 
        "experience_years": DOCTOR_FEE_RANGES[5]["experience_years"], 
        "is_available": DOCTOR_FEE_RANGES[5]["is_available"]
    },
]

def get_doctor_fee_and_experience(doctor_index):
    """Get the doctor's fee and experience years."""
    return DOCTOR_FEE_RANGES[doctor_index]["fee"], DOCTOR_FEE_RANGES[doctor_index]["experience_years"]

def create_appointment(doctor, start_date):
    """Create an appointment for the given doctor and start date."""
    return {
        'id': doctor['id'] + 1,
        'doctor_id': doctor['id'],
        'patient_id': doctor['id'] + 1,
        'date': start_date,
        'fee': doctor['fee'],
        'experience_years': doctor['experience_years']
    }

def generate_appointments(doctors, start_date, number_of_appointments):
    """Generate appointments for the given doctors, start date, and number of appointments."""
    appointments = []
    for doctor in doctors:
        appointment = create_appointment(doctor, start_date)
        appointments.append(appointment)
    return appointments

appointments = generate_appointments(doctors, START_DATE, NUMBER_OF_APPOINTMENTS)