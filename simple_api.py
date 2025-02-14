from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "This is the Home page"

@app.route('/competitor-prices')
def competitor_prices():
    return "Here competitor's prices List is given"

@app.route('/analyze-prices')
def analyze_prices():
    return "Here Analyzed prices are displayed"

@app.route('/recommendations')
def recommendations():
    return "here recommendations are given based on the average prices"


if __name__ == '__main__':
    app.run(debug=True)
