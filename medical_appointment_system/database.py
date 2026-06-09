# database.py

# Define named constants
START_DATE = '2022-01-01'
NUMBER_OF_APPOINTMENTS = 6

# Define doctors
doctors = [
    {
        "id": 1, 
        "name": "Dr. Mounika", 
        "specialization": "Cardiologist", 
        "fee": 500, 
        "experience_years": 10, 
        "is_available": True
    },
    {
        "id": 2, 
        "name": "Dr. Shankar", 
        "specialization": "Dermatologist", 
        "fee": 400, 
        "experience_years": 5, 
        "is_available": True
    },
    {
        "id": 3, 
        "name": "Dr. Mahitha", 
        "specialization": "Pediatrician", 
        "fee": 300, 
        "experience_years": 8, 
        "is_available": False
    },
    {
        "id": 4, 
        "name": "Dr. Spoorthi", 
        "specialization": "General", 
        "fee": 200, 
        "experience_years": 12, 
        "is_available": True
    },
    {
        "id": 5, 
        "name": "Dr. Yashwanth", 
        "specialization": "Cardiologist", 
        "fee": 600, 
        "experience_years": 15, 
        "is_available": True
    },
    {
        "id": 6, 
        "name": "Dr. Keerthi", 
        "specialization": "Pediatrician", 
        "fee": 350, 
        "experience_years": 3, 
        "is_available": True
    },
]

def generate_appointments(doctors, start_date, number_of_appointments):
    appointments = []
    for i in range(1, number_of_appointments + 1):
        appointment = {
            'id': i,
            'doctor_id': doctors[i - 1]['id'],
            'patient_id': i,
            'date': start_date
        }
        appointments.append(appointment)
    return appointments

appointments = generate_appointments(doctors, START_DATE, NUMBER_OF_APPOINTMENTS)