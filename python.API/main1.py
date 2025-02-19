from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)