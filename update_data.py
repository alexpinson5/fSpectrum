import pickle
from datetime import datetime
import matplotlib.pyplot as plt

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
            data = pickle.load(file)
        if isinstance(data, str):  # Check if data is a string
            data = []  # Initialize as an empty list
    except FileNotFoundError:
        data = []

    # Print the entries
    #for entry in data:
        #print(entry)

    return data