import requests

def check_internet_connection():
    try:
        # Send a GET request to a reliable website
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Call the function to check internet connectivity
is_connected = check_internet_connection()

# Print the result
if is_connected:
    print("Internet is connected!")
else:
    print("No internet connection.")