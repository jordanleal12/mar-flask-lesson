from flask import Blueprint, jsonify, request
from init import db
from models.student import Student, students_schema, student_schema

student_bp = Blueprint("student", __name__, url_prefix="/students")


@student_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    # Experiment on how to access from scalar generators
    students_list = db.session.scalars(stmt)
    names = [s.name for s in students_list]
    print(names)
    if data:
        return jsonify(data)
    else:
        return {"message": "No student records found"}, 404


@student_bp.route("/<int:student_id>")
def get_a_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)

    if not student:
        return {"message": "No student record found"}, 404
    data = student_schema.dump(student)
    return jsonify(data)


@student_bp.route("/", methods=["POST"])
def create_a_student():
    body_data = request.get_json()
    new_student = Student(
        name=body_data.get("name"),
        email=body_data.get("email"),
        address=body_data.get("address"),
    )
    db.session.add(new_student)
    db.session.commit()

    data = student_schema.dump(new_student)
    return jsonify(data), 201
