from pymongo import MongoClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Prescription, InternalDoctor, Patient, Drug, RepeatablePrescription
from datetime import datetime
from db import create_connection


def fetch_and_transform_data(session):
    data = []
    # Fetch all prescriptions and join related data
    results = (
        session.query(Prescription, InternalDoctor, Patient, Drug, RepeatablePrescription)
        .join(InternalDoctor, Prescription.internal_doctor_id == InternalDoctor.id)
        .join(Patient, Prescription.patient_id == Patient.id)
        .join(Drug, Prescription.drug_id == Drug.drug_id)
        .outerjoin(RepeatablePrescription, Prescription.prescription_id == RepeatablePrescription.prescription_id) # I'm using outerjoin because not all the prescriptions are repeteable
        .all()
    )

    # Transform each record
    for prescription, doctor, patient, drug, repeatable in results:
        doc = {
            "prescription_id": prescription.prescription_id,
            "prescription_date": prescription.prescription_date.isoformat(),
            "doctor": {
                "id": doctor.id,
                "name": doctor.name,
                "surname": doctor.surname,
            },
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "surname": patient.surname,
                "birthdate": patient.birthdate.isoformat(),
            },
            "drug": {
                "id": drug.drug_id,
                "name": drug.drug_name,
                "strength": drug.drug_strength,
            },
            "directions": prescription.directions,
            "dosage_form": prescription.dosage_form,
            "quantity": prescription.quantity,
        }
        # Add repeatable details if present
        if repeatable:
            doc["repeatable"] = {
                "interval_days": repeatable.interval_days,
                "max_repeats": repeatable.max_repeats,
                "n_time_issued": repeatable.n_time_issued,
            }
        data.append(doc)

    return data


def insert_to_mongo(data, collection):
    for doc in data:
        # Check if a document with the same prescription_id already exists
        if not collection.find_one({"prescription_id": doc["prescription_id"]}):
            collection.insert_one(doc)  # Insert the document if it does not exist

# the same queries that I used for the SQL Alchemy query test
def find_prescriptions_with_doctor_and_patient(collection):
    # Retrieve all prescriptions along with doctor and patient details.
    results = collection.find({}, {
        "prescription_date": 1,
        "doctor": 1,
        "patient": 1,
        "drug": 1,
        "_id": 0  # Exclude MongoDB's internal ID 
    })

    return list(results)

def find_patients_with_repeatable_prescriptions(collection):
    #Retrieve all patients who have repeatable prescriptions.
    results = collection.find({"repeatable": {"$exists": True}}, {
        "patient": 1,
        "repeatable": 1,
        "prescription_date": 1,
        "_id": 0
    })

    return list(results)


def find_most_prescribed_drug(collection):
    #Find the most prescribed drug based on the number of prescriptions.
    pipeline = [
        {"$group": {"_id": "$drug.name", "prescription_count": {"$sum": 1}}},
        {"$sort": {"prescription_count": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))

    return result[0]


if __name__ == "__main__":
    try:
        #Connect to the relational database importing the function from db.py
        engine = create_connection()

        with Session(engine) as session:

            client = MongoClient("mongodb://localhost:27017/")
            db = client["medical_db"]  # Database name
            collection = db["prescriptions"]  # Collection name

            # fetch and transform data
            transformed_data = fetch_and_transform_data(session)

            # insert data into MongoDB
            insert_to_mongo(transformed_data, collection)

            # Doing some queries to check the datas
            print("\n--- Prescriptions with Doctor and Patient Details ---")
            prescriptions = find_prescriptions_with_doctor_and_patient(collection)
            for prescription in prescriptions:
                print(prescription)

            print("\n--- Patients with Repeatable Prescriptions ---")
            repeatable_prescriptions = find_patients_with_repeatable_prescriptions(collection)
            for repeatable in repeatable_prescriptions:
                print(repeatable)

            print("\n--- Most Prescribed Drug ---")
            most_prescribed_drug = find_most_prescribed_drug(collection)
            print(most_prescribed_drug)

    except Exception as e:
        print(f"An error occurred: {e}")