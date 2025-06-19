from client_lib import *
import json
import random
from datetime import datetime

def view_id_athletes():
    athletes = get_all_athletes()
    for athlete in athletes:
        print(f"ID: {athlete['athlete_id']} - Name: {athlete['firstname']} {athlete['lastname']}")

def view_all_athletes():
    athletes = get_all_athletes()
    if not athletes:
        print("No athletes found.")
        return
    for athlete in athletes:
        print(f"-------------------------------")
        print(f"ID: {athlete['athlete_id']}")
        print(f"Name: {athlete['firstname']} {athlete['lastname']}")
        print(f"Username: {athlete['username']}")
        print(f"Location: {athlete.get('city', 'N/A')}, {athlete.get('country', 'N/A')}")
        print(f"Sex: {athlete.get('sex', 'N/A')}")
        print(f"Weight: {athlete.get('weight', 'N/A')} kg")
        print(f"Premium: {'Yes' if athlete.get('premium') else 'No'}")
        print(f"-------------------------------\n")

def view_athlete_details():
    athlete_id = int(input("Enter athlete ID: "))
    athlete = get_athlete(athlete_id)
    if athlete:
        print()
        print(f"Name: {athlete['firstname']} {athlete['lastname']}")
        print(f"Bio: {athlete.get('bio', 'N/A')}")
        print(f"Location: {athlete.get('city', 'N/A')}, {athlete.get('country', 'N/A')}")
        print(f"Weight: {athlete.get('weight', 'N/A')} kg")
        print(f"Sex: {athlete.get('sex', 'N/A')}")
        print(f"Premium: {'Yes' if athlete.get('premium') else 'No'}")
        print(f"Profile Image: {athlete.get('profile')}")
    else:
        print("Athlete not found.")

def add_new_athlete():
    print("\n>> Add Athlete")
    firstname = input("First name: ")
    lastname = input("Last name: ")
    username = input("Username: ")
    sex = input("Sex (M/F): ")
    weight = float(input("Weight (kg): "))
    city = input("City (optional): ") or ""
    country = input("Country (optional): ") or ""
    random_id = random.randint(100000000, 999999999)
    new_athlete = {
        "athlete_id": random_id ,
        "firstname": firstname,
        "lastname": lastname,
        "username": username,
        "sex": sex,
        "weight": weight,
        "city": city,
        "country": country,
        "bio": "",
        "profile": "",
        "profile_medium": "",
        "badge_type_id": 1,
        "resource_state": 2,
        "summit": False,
        "premium": False,
        "follower": None,
        "friend": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    response = add_athlete(new_athlete)

    if response and 'message' in response:
        print("Athlete added successfully!")
    else:
        print("Failed to add athlete.")

def edit_athlete():
    print("\n>> Edit Athlete")
    athlete_id = input("Enter athlete ID: ")

    athlete = get_athlete(athlete_id)
    if not athlete:
        print("Athlete not found.")
        return

    print(f"Editing {athlete['firstname']} {athlete['lastname']}")

    while True:
        print("\nChoose field to edit:")
        print("1. Bio")
        print("2. Weight")
        print("3. Save and exit")
        print("4. Exit without saving")
        choice = input("Enter option number: ")

        if choice == '1':
            new_bio = input("Enter new bio (leave blank to keep current): ")
            if new_bio:
                athlete['bio'] = new_bio
        elif choice == '2':
            new_weight = input("Enter new weight (kg) (leave blank to keep current): ")
            if new_weight:
                try:
                    athlete['weight'] = float(new_weight)
                except ValueError:
                    print("Invalid weight. Please enter a number.")
        elif choice == '3':
            update_athlete(athlete_id, athlete)
            print("Athlete updated successfully!")
            break
        elif choice == '4':
            print("Exiting without saving changes.")
            break
        else:
            print("Invalid choice. Try again.")


def delete_old_athlete():
    print("\n>> Delete Athlete")
    athlete_id = int(input("Enter athlete ID: "))

    athlete = get_athlete(athlete_id)
    if athlete:
        confirm = input(f"Are you sure you want to delete {athlete['firstname']} {athlete['lastname']}? (y/n): ")
        if confirm.lower() == 'y':
            response = delete_athlete(athlete_id)
            if response and 'message' in response:
                print("Athlete added successfully!")
            else:
                print("Failed to add athlete.")
        else:
            print("Deletion cancelled.")
    else:
        print("Athlete not found.")


def view_athlete_summary():
    print("\n>> View Athlete Run Summary")
    athlete_id = int(input("Enter athlete ID: "))

    summary = get_summary_athlete(athlete_id)

    if summary:
        print(f"\nSummary for athlete ID {athlete_id}:")
        print(f"- Total activities:   {summary.get('total_activities', 0)}")
        print(f"- Total distance:     {summary.get('total_distance', 0):.1f} km")
        print(f"- Total elevation:    {summary.get('total_elevation', 0):.1f} m")
        print(f"- Average speed:      {summary.get('average_speed', 0):.2f} m/s")
        print(f"- Average pace:       {summary.get('average_pace', 'N/A')}")
        print(f"- Average heartrate:  {summary.get('average_heartrate', 'N/A')} bpm")
        print(f"- Max heartrate:      {summary.get('max_heartrate', 'N/A')} bpm")
    else:
        print("Athlete not found or failed to retrieve summary.")
