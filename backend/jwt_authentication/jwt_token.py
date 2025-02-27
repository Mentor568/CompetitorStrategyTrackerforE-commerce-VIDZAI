from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
import pytz
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bb1bd16a70ae425ba6f842d4646b8716'
timezone = pytz.timezone('Asia/Kolkata')

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 403
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.payload = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 403
        return func(*args, **kwargs)
    return decorated

# Home route
@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login123.html')
    else:
        return "Logged in successfully"

# Public route
@app.route("/public")
def public():
    return 'For Public'
"perform query http://127.0.0.1:5000/auth?token=your_token"
# Authentication route
@app.route('/auth')
@token_required
def auth():
    return 'JWT verified successfully'

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        expiration = datetime.now(timezone) + timedelta(seconds=120)
        expiration_str = expiration.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': expiration_str  # Convert expiration to a string
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm="Authentication failed"'})

if __name__ == "__main__":
    app.run(debug=True)
