from utils_athletes import *
from utils_activities import *
from utils_analysis import *

def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Athlete Management")
        print("2. Activity Management")
        print("3. Analysis & Advanced Functions")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            athlete_management_menu()
        elif choice == '2':
            activity_management_menu()
        elif choice == '3':
            analysis_menu()
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

def athlete_management_menu():
    while True:
        print("\n=== Athlete Management Menu ===")
        print("0. View all the athletes IDs")
        print("1. View all athletes")
        print("2. View athlete details")
        print("3. Add athlete")
        print("4. Edit athlete")
        print("5. Delete athlete")
        print("6. View athlete Run summary")
        print("7. Go back to main menu")

        choice = input("Select an option: ")
        if choice == '0':
            view_id_athletes()
        elif choice == '1':
            view_all_athletes()
        elif choice == '2':
            view_athlete_details()
        elif choice == '3':
            add_new_athlete()
        elif choice == '4':
            edit_athlete()
        elif choice == '5':
            delete_old_athlete()
        elif choice == '6':
            view_athlete_summary()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please select again.")

def activity_management_menu():
    while True:
        print("\n=== Activity Management Menu ===")
        print("0. View all the activities IDs")
        print("1. View all activities")
        print("2. Show activity details")
        print("3. Add activity")
        print("4. Edit activity")
        print("5. Delete activity")
        print("6. Go back to main menu")

        choice = input("Select an option: ")
        if choice == '0':
            view_id_activities()
        elif choice == '1':
            view_all_activities()
        elif choice == '2':
            show_activity_details()
        elif choice == '3':
            add_activity_interactive()
        elif choice == '4':
            edit_activity()
        elif choice == '5':
            delete_old_activity()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please select again.")

def analysis_menu():
    while True:
        print("\n=== Analysis & Advanced Functions Menu ===")
        print("1. Compare athletes")
        print("2. List athlete's activities")
        print("3. Athlete statistics overview")
        print("4. Visualize routes and streams")
        print("5. Back to main menu")

        choice = input("Select an option: ")

        if choice == '1':
            compare_athletes()
        elif choice == '2':
            list_athlete_activities()
        elif choice == '3':
            athlete_statistics_overview()
        elif choice == '4':
            visualize_routes_and_streams()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    main_menu()