from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models import Student, students_schema, student_schema

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
    try:
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
    except IntegrityError as err:
        match err.orig.pgcode:
            case errorcodes.NOT_NULL_VIOLATION:
                return {
                    "message": f"Required field <{err.orig.diag.column_name}> cannot be null."
                }, 400
            case errorcodes.UNIQUE_VIOLATION:
                return {"message": "Email must be unique"}, 400
            case _:
                return {"message": "Unexpected error occured"}, 400


@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {"message": f"Student '{student.name}' has been deleted successfully"}
    else:
        return {"message": f"Student '{student_id}' does not exist"}, 404


@student_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    if student:
        body_data = request.get_json()

        student.name = body_data.get("name") or student.name
        student.email = body_data.get("email") or student.email
        student.address = body_data.get("address") or student.address
        db.session.commit()
        return jsonify(student_schema.dump(student))
    else:
        return {"message": f"Student with id {student_id} does not exist."}, 404
