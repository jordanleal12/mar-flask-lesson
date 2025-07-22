from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models import Teacher, teachers_schema, teacher_schema


teacher_bp = Blueprint("teacher", __name__, url_prefix="/teachers")


@teacher_bp.route("/")
def get_teachers():
    print("Route was hit")
    stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt).all()
    print(f"Found teachers: {teachers_list}")
    data = teachers_schema.dump(teachers_list)
    print(f"Serialized data: {data}")
    if data:
        return jsonify(data)
    else:
        return {"message": "No teacher records found"}, 404


@teacher_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)

    if not teacher:
        return {"message": "No teacher record found"}, 404
    data = teacher_schema.dump(teacher)
    return jsonify(data)


@teacher_bp.route("/", methods=["POST"])
def create_a_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address"),
        )
        db.session.add(new_teacher)
        db.session.commit()

        data = teacher_schema.dump(new_teacher)
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


@teacher_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher '{teacher.name}' has been deleted successfully"}
    else:
        return {"message": f"Teacher '{teacher_id}' does not exist"}, 404


@teacher_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        body_data = request.get_json()

        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
        db.session.commit()
        return jsonify(teacher_schema.dump(teacher))
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist."}, 404
