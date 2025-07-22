from flask import Blueprint
from init import db
from models import Student, Teacher

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_table():
    db.create_all()
    print("tables created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("tables drop")


@db_commands.cli.command("seed")
def seed_tables():
    students = [
        Student(name="Alice", email="alice@email.com", address="Sydney"),
        Student(name="Bob", email="bob@email.com", address="Melbourne"),
    ]
    db.session.add_all(students)
    teachers = [
        Teacher(name="TeacherA", department="Science", address="Sydney"),
        Teacher(name="TeacherB", department="Management", address="Perth"),
    ]
    db.session.add_all(teachers)
    db.session.commit()
    print("tables seeded")
