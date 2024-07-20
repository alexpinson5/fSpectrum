import requests

def check_internet_connection():
    try:
        # Send a GET request to a reliable website
        response = requests.get("http://clients3.google.com/generate_204", timeout=5)
        return True
    except requests.ConnectionError:
        return False