from flask import Flask, jsonify
import requests
app = Flask(__name__)
def fetch_github_api():
    url = "https://api.github.com"
    response = requests.get(url)
    return response.json()

@app.route('/github', methods=['GET'])
def github_api():
    """API endpoint to fetch GitHub API data"""
    return jsonify(fetch_github_api())

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, Faiza's API is working!"})

if __name__ == '__main__':
    app.run(debug=True)
