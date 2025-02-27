from flask import Flask, request, jsonify, render_template_string # Import necessary modules from Flask

import pytz # Import pytz for timezone handling
from pymongo import MongoClient # Import MongoDB client
from functools import wraps # Import wraps for decorator function

app = Flask(__name__) # Initialize the Flask application
app.config['SECRET_KEY'] = 'bb1bd16a70ae425ba6f842d4646b8716' # Set a secret key for the Flask app
timezone = pytz.timezone('Asia/Kolkata') # Define the timezone

# Initialize MongoDB client and select the database and collection
client = MongoClient('mongodb://localhost:27017/') # Replace with your MongoDB URI if different
db = client['rbac_db']
users_collection = db['users']

def role_required(role):
    """Decorator function to check if the user has the required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            username = request.args.get('username')
            if not username:
                return jsonify({'Alert!': 'Username is missing'}), 403
            
            user = users_collection.find_one({'username': username})
            
            if not user:
                return jsonify({'Alert!': 'User not found'}), 403
            if user['role'] != role:
                return jsonify({'Alert!': f'Role {role} is required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/add_user', methods=['POST'])
def add_user():
    """Route to add a new user with a role"""
    data = request.get_json()
    username = data.get('username')
    role = data.get('role')
    
    if not username or not role:
        return jsonify({'Alert!': 'Username and role are required'}), 400
    
    users_collection.insert_one({'username': username, 'role': role})
    
    return jsonify({'Success': f'User {username} with role {role} added'}), 201
"perform the queries http://127.0.0.1:5000/user?username=given_name"
@app.route('/admin')
@role_required('admin')
def admin():
    """Route accessible only by users with the 'admin' role"""
    return 'Welcome, Admin!'
"perform the query http://127.0.0.1:5000/admin?username=given_name"
@app.route('/user')
@role_required('user')
def user():
    """Route accessible only by users with the 'user' role"""
    return 'Welcome, User!'

@app.route('/')
def index():
    """Default route"""
    return 'Welcome to the RBAC Application!'

@app.errorhandler(404)
def not_found(e):
    """Custom 404 error handler"""
    return jsonify({'Error': 'Not Found', 'Message': 'The requested URL was not found on the server.'}), 404

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode
