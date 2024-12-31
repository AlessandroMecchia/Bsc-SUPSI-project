from sqlalchemy.orm import Session
from sqlalchemy import func, select, text
from models import InternalDoctor, Patient, Prescription, Drug, RepeatablePrescription
from db import create_connection, Model
from datetime import datetime

def create_new_tables(engine):
    Model.metadata.create_all(
        engine,
        tables=[
            Prescription.__table__,
            Drug.__table__,
            RepeatablePrescription.__table__
        ]
    )

def populate_data(session):
    # Populate the database with initial data only if the tables are empty.
    # Add Drugs
    if session.query(Drug).first() is None:
        drugs = [
            Drug(drug_id=1, drug_name="Paracetamolo", drug_strength="500mg"),
            Drug(drug_id=2, drug_name="Ibuprofene", drug_strength="200mg"),
            Drug(drug_id=3, drug_name="Fentanyl", drug_strength="5mg"),
            Drug(drug_id=4, drug_name="Voltaren", drug_strength="200mg")
        ]
        session.add_all(drugs)
        session.commit()

    # Add Prescriptions
    if session.query(Prescription).first() is None:
        prescriptions = [
            # Patient 1, Prescription 1
            Prescription(
                prescription_id=1,
                prescription_date=datetime(2023, 6, 15),
                internal_doctor_id=1,
                patient_id=1,
                drug_id=1,  # Paracetamolo
                directions="Take one tablet every 8 hours",
                dosage_form="Tablet",
                quantity=30
            ),
            # Patient 2, Prescription 2
            Prescription(
                prescription_id=2,
                prescription_date=datetime(2023, 7, 20),
                internal_doctor_id=2,
                patient_id=2,
                drug_id=2,  # Ibuprofene
                directions="Take two tablets every 6 hours with food",
                dosage_form="Tablet",
                quantity=60
            ),
            # Patient 1, Prescription 3 (repeatable)
            Prescription(
                prescription_id=3,
                prescription_date=datetime(2023, 8, 1),
                internal_doctor_id=1,
                patient_id=1,
                drug_id=3,  # Fentanyl
                directions="Apply one patch every 3 days",
                dosage_form="Patch",
                quantity=10
            ),
            # Patient 3, Prescription 4 (non-repeatable)
            Prescription(
                prescription_id=4,
                prescription_date=datetime(2023, 9, 1),
                internal_doctor_id=3,
                patient_id=3,
                drug_id=4,  # Voltaren
                directions="Take one tablet every 12 hours",
                dosage_form="Tablet",
                quantity=20
            ),
            # Patient 2, Prescription 5 (repeatable with the same drug)
            Prescription(
                prescription_id=5,
                prescription_date=datetime(2023, 10, 5),
                internal_doctor_id=2,
                patient_id=2,
                drug_id=2,  # Ibuprofene (same drug as prescription_id=2)
                directions="Take one tablet every 12 hours",
                dosage_form="Tablet",
                quantity=90
            )
        ]
        session.add_all(prescriptions)
        session.commit()

    # Add Repeatable Prescriptions
    if session.query(RepeatablePrescription).first() is None:
        repeatables = [
            # Repeatable for Prescription 1
            RepeatablePrescription(
                repeatable_id=1,
                prescription_id=1,
                interval_days=30,
                max_repeats=3,
                n_time_issued=1
            ),
            # Repeatable for Prescription 3
            RepeatablePrescription(
                repeatable_id=2,
                prescription_id=3,
                interval_days=3,
                max_repeats=10,
                n_time_issued=2
            ),
            # Repeatable for Prescription 5 (same drug as prescription_id=2)
            RepeatablePrescription(
                repeatable_id=3,
                prescription_id=5,
                interval_days=15,
                max_repeats=5,
                n_time_issued=1
            )
        ]
        session.add_all(repeatables)
        session.commit()

    # Add Repeatable Prescriptions
    if session.query(RepeatablePrescription).first() is None:
        repeatables = [
            # Repeatable for Prescription 1
            RepeatablePrescription(
                repeatable_id=1,
                prescription_id=1,
                interval_days=30,
                max_repeats=3,
                n_time_issued=1
            ),
            # Repeatable for Prescription 3
            RepeatablePrescription(
                repeatable_id=2,
                prescription_id=3,
                interval_days=3,
                max_repeats=10,
                n_time_issued=2
            )
        ]
        session.add_all(repeatables)
        session.commit()

def find_prescriptions_with_doctor_and_patient(session):
    # Retrieve all prescriptions along with doctor and patient details
    # Returns a liist of tuples (prescription, doctor, patient, drug)
    stmt = (
        select(Prescription, InternalDoctor, Patient, Drug)
        .join(InternalDoctor, Prescription.internal_doctor_id == InternalDoctor.id)
        .join(Patient, Prescription.patient_id == Patient.id)
        .join(Drug, Prescription.drug_id == Drug.drug_id)
    )
    return session.execute(stmt).all()

def find_patients_with_repeatable_prescriptions(session):
    # Retrieve all patients who have repeatable prescriptions
    # Returns a List of tuples (patient, repeatable, prescription)
    stmt = (
        select(Patient, RepeatablePrescription, Prescription)
        .join(Prescription, Prescription.patient_id == Patient.id)
        .join(RepeatablePrescription, RepeatablePrescription.prescription_id == Prescription.prescription_id)
    )
    return session.execute(stmt).all()

def find_most_prescribed_drug(session):
    # Find the most prescribed drug based on the number of prescriptions
    # it returns a tuple (drug_name, prescription_count) or None if no data
    stmt = (
        select(Drug.drug_name, func.count(Prescription.prescription_id).label("prescription_count"))
        .join(Prescription, Drug.drug_id == Prescription.drug_id)
        .group_by(Drug.drug_name)
        .order_by(func.count(Prescription.prescription_id).desc())
        .limit(1)
    )
    return session.execute(stmt).first()




if __name__ == "__main__":
    try:
        # Create database connection
        engine = create_connection()
        create_new_tables(engine)

        with Session(engine) as session:
            # Populate the database with initial data
            populate_data(session)

            #do the query
            print("\n--- Prescriptions with Doctor and Patient Details ---")
            prescriptions = find_prescriptions_with_doctor_and_patient(session)
            for prescription, doctor, patient, drug in prescriptions:
                print(f"Prescription ID: {prescription.prescription_id}, Date: {prescription.prescription_date}")
                print(f"Doctor: Dr. {doctor.name} {doctor.surname}")
                print(f"Patient: {patient.name} {patient.surname}")
                print(f"Drug: {drug.drug_name} ({drug.drug_strength})")
                print("----")

            print("\n--- Patients with Repeatable Prescriptions ---")
            repeatables = find_patients_with_repeatable_prescriptions(session)
            for patient, repeatable, prescription in repeatables:
                print(f"Patient: {patient.name} {patient.surname}")
                print(f"Prescription ID: {prescription.prescription_id}")
                print(f"Repeatable: Interval = {repeatable.interval_days} days, Max Repeats = {repeatable.max_repeats}")
                print("----")

            print("\n--- Most Prescribed Drug ---")
            most_prescribed = find_most_prescribed_drug(session)
            if most_prescribed:
                print(f"Drug: {most_prescribed[0]}, Prescriptions: {most_prescribed[1]}")
            else:
                print("No prescriptions found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")