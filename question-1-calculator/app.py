from flask import Flask, jsonify
from collections import deque
import requests

app=Flask(__name__)

window_size = 20
numbers_window = deque()

def fetch_number(number_id):
    url = f"http://20.244.56.144/test/{number_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('number',[])
    else:
        return []
    
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    global numbers_window
    
    numbers_fetched = fetch_numbers(number_id)
    
    for num in numbers_fetched:
        if num not in numbers_window:
            numbers_window.append(num)
            if len(numbers_window) > window_size:
                numbers_window.popleft()

    avg = 0
    if len(numbers_window) == window_size:
        avg = calculate_average(numbers_window)
    
    response = {
        "windowPrevState":list(numbers_window),
        "windowCurrState":list(numbers_window),
        "numbers": numbers_fetched,
        "avg":avg
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)