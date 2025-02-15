from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    if not students:
        return jsonify({"message": "No students found"}), 404
    return jsonify([{"id": stu.id, "name": stu.name, "course": stu.course} for stu in students])

# GET a student by ID
@app.route('/students/<int:stu_id>', methods=['GET'])
def get_student(stu_id):
    student = Student.query.get(stu_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    return jsonify({"id": student.id, "name": student.name, "course": student.course})

# POST (Add a new student)
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data["name"], course=data["course"])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added"}), 201

# PUT (Update a student)
@app.route('/students/<int:stu_id>', methods=['PUT'])
def update_student(stu_id):
    student = Student.query.get(stu_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    data = request.json
    student.name = data.get("name", student.name)
    student.course = data.get("course", student.course)
    db.session.commit()
    return jsonify({"message": "Student updated"})

# DELETE a student
@app.route('/students/<int:stu_id>', methods=['DELETE'])
def delete_student(stu_id):
    student = Student.query.get(stu_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"})

if __name__ == '__main__':
    app.run(debug=True)
