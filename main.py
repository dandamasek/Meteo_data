from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/get-data', methods=['GET'])
def get_data():
    # Define the URL
    url = "https://opendata.chmi.cz/hydrology/now/data/0-203-1-001000.json"
    
    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://opendata.chmi.cz/hydrology/now/data/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "If-Modified-Since": "Fri, 27 Sep 2024 15:00:09 GMT",
        "If-None-Match": '"66f6c879-1f75"',
        "Priority": "u=0, i"
    }
    
    try:
        # Make the GET request to the given URL with the specified headers
        response = requests.get(url, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            # Return the JSON data from the response
            return jsonify(response.json())
        else:
            # If the response has a different status, return an error
            return jsonify({"error": f"Failed to fetch data, status code: {response.status_code}"})
    
    except Exception as e:
        # In case of an exception, return the error message
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
