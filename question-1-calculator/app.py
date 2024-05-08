from flask import Flask, jsonify, request
from collections import deque
import requests

app = Flask(__name__)

window_size = 10
numbers_window = deque()

def fetch_numbers(number_type):
    try:
        access_token = ""
        url = f"http://20.244.56.144/test/{number_type}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching numbers: {e}")
        return []
    except Exception as e:
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

   
    numbers_fetched = fetch_numbers(number_type)

    for num in numbers_fetched:
        if num not in numbers_window:
            numbers_window.append(num)
            if len(numbers_window) > window_size:
                numbers_window.popleft()

    avg = calculate_average(numbers_window)

    response = {
        "windowPrevState": list(numbers_window),
        "windowCurrState": list(numbers_window),
        "numbers": numbers_fetched,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
