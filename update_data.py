import pickle
from datetime import datetime

def log_true():
    # Prepare the data for insertion
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection_status = 1

    # Load existing data from the pickle file, if any
    try:
        with open("data.pickle", "rb") as file:
            existing_data = pickle.load(file)
    except FileNotFoundError:
        existing_data = []

    # Add the new entry to the data list
    entry = {"datetime": current_time, "connection": connection_status}
    existing_data.append(entry)

    # Save the updated data back to the pickle file
    with open("data.pickle", "wb") as file:
        pickle.dump(existing_data, file)

    print("Entry added successfully.")

def log_false():
    # Prepare the data for insertion
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection_status = 0

    # Load existing data from the pickle file, if any
    try:
        with open("data.pickle", "rb") as file:
            existing_data = pickle.load(file)
    except FileNotFoundError:
        existing_data = []

    # Add the new entry to the data list
    entry = {"datetime": current_time, "connection": connection_status}
    existing_data.append(entry)

    # Save the updated data back to the pickle file
    with open("data.pickle", "wb") as file:
        pickle.dump(existing_data, file)

    print("Entry added successfully.")

def print_entries_from_pickle():
    try:
        with open("data.pickle", "rb") as file:
            entries = pickle.load(file)

        if isinstance(entries, list):
            print("Datetime\t\t\tConnection")
            print("-----------------------------------------")
            for entry in entries:
                if isinstance(entry, dict):
                    datetime_str = entry.get("datetime", "")
                    connection = entry.get("connection", False)

                    if isinstance(datetime_str, str):
                        print(f"{datetime_str}\t{connection}")
                    else:
                        print("Invalid datetime format in pickle file.")
                else:
                    print("Invalid entry format in pickle file.")
        else:
            print("Invalid data format in pickle file.")
    except FileNotFoundError:
        print("Pickle file not found.")
