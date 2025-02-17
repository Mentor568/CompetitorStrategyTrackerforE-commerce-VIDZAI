from flask import Flask, request, jsonify  


app = Flask(__name__)


students = [
    {"id": 1, "name": "Alice", "age": 21},
    {"id": 2, "name": "Bob", "age": 22},
    {"id": 3, "name": "Charlie", "age": 23}
]


@app.route('/students', methods=['POST'])
def add_student():
    data = request.json 
    students.append(data)  
    return jsonify({"message": "Student added successfully", "students": students}), 201  


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": students})  

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    for student in students:  
        if student["id"] == student_id:
            student.update(request.json)  
            return jsonify({"message": "Student updated", "students": students})  
    return jsonify({"error": "Student not found"}), 404 

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student) 
            return jsonify({"message": "Student deleted", "students": students})  
    return jsonify({"error": "Student not found"}), 404  


if __name__ == '__main__':
    app.run(debug=True)  

