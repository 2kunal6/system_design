from enum import Enum
from datetime import datetime

class Speciality(Enum):
    Cardiologist = 1
    Dermatologist = 2
    Orthopedic = 3
    General = 4
    Physician = 5

class Doctor:
    def __init__(self, id, speciality):
        self.id = id
        #self.rating = 2
        self.speciality = speciality
        self.availabilities = set()
    def add_availability(self, start_time, end_time):
        self.availabilities.add((datetime.strptime(start_time, '%Y%m%d %H:%M'), datetime.strptime(end_time, '%Y%m%d %H:%M')))


class Patient:
    def __init__(self, id):
        self.id = id

class Booking:
    def __init__(self, booking_id, patient_id, doctor_id, start_time, end_time):
        self.booking_id = booking_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.start_time = start_time
        self.end_time = end_time
        self.is_cancelled = False

    def cancel_booking(self):
        self.is_cancelled = True

from abc import ABC, abstractmethod
class Isearch:
    @abstractmethod
    def search(self):
        pass

class RatingBasedSearch(Isearch):
    def search(self):
        pass
'''
class SearchManager:
    def __init__(self):
'''
class FlipMed:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.doctors = []
        self.patients = []
        self.bookings = []

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def add_patient(self, patient):
        self.patients.append(patient)

    def check_availability(self, doctor_id, start_time, end_time):
        for doctor in self.doctors:
            if(doctor.id == doctor_id):
                for availability in doctor.availabilities:
                    if(availability[0] == start_time and availability[1] == end_time):
                        return True
        return False

    # concurrency
    def book_appointment(self, booking_id, patient_id, doctor_id, start_time, end_time):
        start_time = datetime.strptime(start_time, '%Y%m%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y%m%d %H:%M')
        is_available = self.check_availability(doctor_id, start_time, end_time)
        if(not is_available):
            print('Not available')
        else:
            booking = Booking(booking_id, patient_id, doctor_id, start_time, end_time)
            self.bookings.append(booking)


    def cancel_appointment(self, booking_id):
        for booking in self.bookings:
            if(booking.id == booking_id):
                booking.cancel_booking()

    def search_doctors(self, speciality):
        speciality_doctors = []
        for doctor in self.doctors:
            if(doctor.speciality == speciality):
                speciality_doctors.append(doctor)
        return speciality_doctors

flipmed = FlipMed()
patient_1 = Patient(1)
doctor_1 = Doctor(1, Speciality.General)
doctor_1.add_availability('20250101 09:30', '20250101 10:00')

flipmed.add_doctor(doctor_1)
flipmed.add_patient(patient_1)

doctors = flipmed.search_doctors(Speciality.General)
for doctor in doctors:
    print(doctor.id)
flipmed.book_appointment(1, 1, 1, '20250101 09:30', '20250101 10:00')
print(flipmed.bookings[0])