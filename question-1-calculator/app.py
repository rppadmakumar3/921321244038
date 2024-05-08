from flask import Flask, jsonify, request
from collections import deque
import requests

app = Flask(__name__)

# Global variables for window size and numbers window
window_size = 10
numbers_window = deque()

def fetch_numbers(number_type):
    try:
        access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE1MTYwODA4LCJpYXQiOjE3MTUxNjA1MDgsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjlmMDgyNDdkLTcxM2EtNDliYi1hZWM3LTBjZDYwYTdmNTY0MiIsInN1YiI6InBhZG1ha3VtYXJyMjFjYkBwc25hY2V0LmVkdS5pbiJ9LCJjb21wYW55TmFtZSI6IlBTTkEgQ29sbGVnZSBvZiBFbmdpbmVlcmluZyBhbmQgVGVjaG5vbG9neSIsImNsaWVudElEIjoiOWYwODI0N2QtNzEzYS00OWJiLWFlYzctMGNkNjBhN2Y1NjQyIiwiY2xpZW50U2VjcmV0IjoiQXVScHRPWmhmdkhVTUNTSSIsIm93bmVyTmFtZSI6IlBhZG1ha3VtYXIiLCJvd25lckVtYWlsIjoicGFkbWFrdW1hcnIyMWNiQHBzbmFjZXQuZWR1LmluIiwicm9sbE5vIjoiOTIxMzIxMjQ0MDM4In0._RplEFKra5aXEN_gHKZ1Wfk7g68f0NmGt0Gcy5cZyUg"
        url = f"http://20.244.56.144/test/{number_type}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        return response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        # Log the error and return an empty list
        app.logger.error(f"Error fetching numbers: {e}")
        return []
    except Exception as e:
        # Log other unexpected errors
        app.logger.error(f"Unexpected error: {e}")
        return []

def calculate_average(numbers):
    try:
        if len(numbers) == 0:
            return 0
        return sum(numbers) / len(numbers)
    except ZeroDivisionError:
        app.logger.error("Division by zero error in calculating average")
        return 0

@app.route('/numbers/<string:number_type>', methods=['GET'])
def get_numbers(number_type):
    global numbers_window

    # Fetch numbers from third-party server based on number_type
    numbers_fetched = fetch_numbers(number_type)

    # Update numbers window and calculate average
    for num in numbers_fetched:
        if num not in numbers_window:
            numbers_window.append(num)
            if len(numbers_window) > window_size:
                numbers_window.popleft()

    avg = calculate_average(numbers_window)

    # Construct and return JSON response
    response = {
        "windowPrevState": list(numbers_window),
        "windowCurrState": list(numbers_window),
        "numbers": numbers_fetched,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
