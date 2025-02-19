import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    app.logger.info(f"Fetching user data for user_id: {user_id}")

    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)
