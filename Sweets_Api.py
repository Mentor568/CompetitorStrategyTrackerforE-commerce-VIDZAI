from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
sweets = [
    {"id": 1, "name": "Chocolate", "price": 50},
    {"id": 2, "name": "Gulab Jamun", "price": 30},
    {"id": 3, "name": "Laddu", "price": 20}
]

# Get all sweets
@app.route('/sweets', methods=['GET'])
def get_sweets():
    return jsonify(sweets)

# Get a sweet by ID
@app.route('/sweets/<int:sweet_id>', methods=['GET'])
def get_sweet(sweet_id):
    sweet = next((s for s in sweets if s["id"] == sweet_id), None)
    if sweet:
        return jsonify(sweet)
    return jsonify({"message": "Sweet not found"}), 404

# Search for Gulab Jamun
@app.route('/search/gulab_jamun', methods=['GET'])
def search_gulab_jamun():
    sweet = next((s for s in sweets if s["name"].lower() == "gulab jamun"), None)
    if sweet:
        return jsonify(sweet)
    return jsonify({"message": "Gulab Jamun not found"}), 404

# Add a new sweet
@app.route('/sweets', methods=['POST'])
def add_sweet():
    new_sweet = request.json
    new_sweet["id"] = len(sweets) + 1
    sweets.append(new_sweet)
    return jsonify(new_sweet), 201

# Update a sweet
@app.route('/sweets/<int:sweet_id>', methods=['PUT'])
def update_sweet(sweet_id):
    sweet = next((s for s in sweets if s["id"] == sweet_id), None)
    if not sweet:
        return jsonify({"message": "Sweet not found"}), 404
    
    data = request.json
    sweet.update(data)
    return jsonify(sweet)

# Delete a sweet
@app.route('/sweets/<int:sweet_id>', methods=['DELETE'])
def delete_sweet(sweet_id):
    global sweets
    sweets = [s for s in sweets if s["id"] != sweet_id]
    return jsonify({"message": "Sweet deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
 output:
{
    "id": 2,
    "name": "Gulab Jamun",
    "price": 30
                 }
                  
