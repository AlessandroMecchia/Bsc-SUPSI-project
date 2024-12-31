# models.py
from typing import List, Optional
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date, Column, Integer
from db import Model

class Specialization(Model):
    __tablename__ = 'specialization'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # Relationships - corrected names to match the back_populates in related models
    internal_doctors = relationship("InternalDoctor", back_populates="specialization")
    external_doctors = relationship("ExternalDoctor", back_populates="specialization")
    diagnoses = relationship("Diagnosis", back_populates="specialization")

    def __repr__(self):
        return f"Specialization(id={self.id}, name={self.name})"


class DoctorMixin:
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    specialization_id = Column('specialization', Integer, ForeignKey('specialization.id'), nullable=False)


class InternalDoctor(DoctorMixin, Model):
    __tablename__ = 'internal_doctor'

    # Relationships
    specialization = relationship("Specialization", back_populates="internal_doctors")
    visits = relationship("Visit", back_populates="internal_doctor")

    prescriptions = relationship('Prescription', back_populates='internal_doctor')

    def __repr__(self):
        return f"InternalDoctor(id={self.id}, name={self.name}, surname={self.surname})"



class ExternalDoctor(DoctorMixin, Model):
    __tablename__ = 'external_doctor'

    street = Column(String(50))
    postcode = Column(String(10))
    city = Column(String(50))

    # Relationships
    specialization = relationship("Specialization", back_populates="external_doctors")
    visits = relationship("Visit", back_populates="external_doctor")

    def __repr__(self):
        return f"ExternalDoctor(id={self.id}, name={self.name}, surname={self.surname})"


class Diagnosis(Model):
    __tablename__ = 'diagnosis'

    code = Column(Integer, primary_key=True)
    text = Column(String(100))
    specialization_id = Column('specialization', Integer, ForeignKey('specialization.id'), nullable=False)

    # Relationships
    specialization = relationship("Specialization", back_populates="diagnoses")
    reports = relationship("Report", back_populates="diagnosis")

    def __repr__(self):
        return f"Diagnosis(code={self.code}, text={self.text})"


class Patient(Model):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    birthdate = Column(Date)
    street = Column(String(50))
    postcode = Column(String(10))
    city = Column(String(50))

    # Relationships
    visits = relationship("Visit", back_populates="patient")
    prescriptions = relationship('Prescription', back_populates='patient')

    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, surname={self.surname})"


class Visit(Model):
    __tablename__ = 'visit'

    v_number = Column(Integer, primary_key=True)
    v_date = Column(Date)
    internal_doctor_id = Column('internal_doctor', Integer, ForeignKey('internal_doctor.id'), nullable=False)
    external_doctor_id = Column('external_doctor', Integer, ForeignKey('external_doctor.id'), nullable=False)
    patient_id = Column('patient', Integer, ForeignKey('patient.id'), nullable=False)

    # Relationships
    internal_doctor = relationship("InternalDoctor", back_populates="visits")
    external_doctor = relationship("ExternalDoctor", back_populates="visits")
    patient = relationship("Patient", back_populates="visits")
    reports = relationship("Report", back_populates="visit")

    def __repr__(self):
        return f"Visit(v_number={self.v_number}, v_date={self.v_date})"


class Report(Model):
    __tablename__ = 'report'

    visit_id = Column('visit', Integer, ForeignKey('visit.v_number'), primary_key=True)
    diagnosis_id = Column('diagnosis', Integer, ForeignKey('diagnosis.code'), primary_key=True)

    # Relationships
    visit = relationship("Visit", back_populates="reports")
    diagnosis = relationship("Diagnosis", back_populates="reports")

    def __repr__(self):
        return f"Report(visit_id={self.visit_id}, diagnosis_id={self.diagnosis_id})"
    
# added classes Prescription, Repeatableprescription and drug
# new class to manage the prescription
class Prescription(Model):
    __tablename__ = 'prescription'

    prescription_id = Column(Integer, primary_key=True)
    prescription_date = Column(Date)
    internal_doctor_id = Column('internal_doctor', Integer, ForeignKey('internal_doctor.id'), nullable=False)
    patient_id = Column('patient', Integer, ForeignKey('patient.id'), nullable=False)
    drug_id = Column(Integer, ForeignKey('drug.drug_id'), nullable=False)
    directions = Column(String(500), nullable=False)
    dosage_form = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)

    # relationship with internal doctor (many-to-one)
    internal_doctor = relationship('InternalDoctor', back_populates='prescriptions')

    #relationship with patient (many-to-one)
    patient = relationship('Patient', back_populates='prescriptions')

    #relationship with drug (many-to-one)
    drug = relationship('Drug', back_populates='prescriptions')

    #relationship with repetition (one-to-one)
    repeatable_info = relationship('RepeatablePrescription', back_populates='prescription')


# new class to handle the repetition of the prescription
class RepeatablePrescription(Model):
    __tablename__ = 'repeatable_prescriptions'

    repeatable_id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey('prescription.prescription_id'), nullable=False)
    interval_days = Column(Integer, nullable=False)  
    max_repeats = Column(Integer, nullable=False)
    n_time_issued = Column(Integer, default=0)

    # relationship with prescription
    prescription = relationship('Prescription', back_populates='repeatable_info')

# new class to manage the drug
class Drug(Model):
    __tablename__ = 'drug'
    
    drug_id = Column(Integer, primary_key=True)
    drug_name = Column(String(255), nullable=False)
    drug_strength = Column(String(255), nullable=False)  

    # Relationship with Prescription (one-to-many)
    prescriptions = relationship('Prescription', back_populates='drug')

    