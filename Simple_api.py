from flask import Flask

app = Flask(__name__)

data = {
    "message": "Hello, this is a simple API!",
    "status": "success"
}

@app.route('/')
def home():
    return str(data)  

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}! Welcome to our API."

if __name__ == '__main__':
    app.run(debug=True)
