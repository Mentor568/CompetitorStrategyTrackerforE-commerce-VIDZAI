from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory database (list of users)
users = []

@app.route('/users', methods=['GET'])
def get_users():
    """Returns the list of all users"""
    return jsonify({"users": users})

@app.route('/users', methods=['POST'])
def add_user():
    """Adds a new user to the list"""
    data = request.get_json()
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400

    user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(user)
    return jsonify({"message": "User added successfully", "user": user}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Fetch a specific user by ID"""
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify({"user": user})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
