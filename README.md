# Creating an LMS app with entities

- Student
- Teacher
- Courses
- Enrollments (junction table)

To run the server successfully, here are the steps you need to perform:

- create a .env file with the variables included in .env.example

  - DATABASE_URI with a connection string to your chosen database, e.g. postgres

- ensure that a local database exists by making one in the postgres shell
  - enter the postgres shell
    - MacOS: run the `psql` command
    - Linux & WSL: run the `sudo -u postgres psql` command
  - list all existing databases by running `\l`
  - if the database you want to use does not currently exist, create it by running `CREATE DATABASE lms_db;`
  - check that it exists by running `\l` again
  - connect to the database you want to use with `\c lms_db`
- ensure that a postgres shell user that has permissions to work with your database
  - in the postgres shell, run `CREATE USER lms_dev WITH PASSWORD '123456';`
  - grant the user the permissions needed to work with the database, run `GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_dev;`
  - grant db schema permissions to the user as well, run `GRANT ALL ON SCHEMA public TO lms_dev;`
- exit the postgres shell with `\q`

- create a .flaskenv file and define: FLASK_APP=main

- make a virtual environment

  - run python3 -m venv .venv
  - activate venv with:
    - MacOs, Linux & WSL : `source .venv/bin/activate`
    - Windows: `.venv/Scripts/activate`
  - set the VSCode Python interpreter to the venv Python binary
    - CTRL + Shift + P to open up the command palette
    - Select interpreter starting with `.venv` path

- Install dependencies within the activated virtual environment with: `pip install -r ./requirements.txt`

- Ensure that the flask app database exists and has any seed data that it's meant to have

  - check the source code for CLI commands, e.g. `./controllers/cli_controller.py`
  - run the commands need to drop, create and seed tables

- flask run to run the server

- OPTIONAL: set flask debug and a manual PORT value into `.flaskenv`:
  - `FLASK_DEBUG=1`
  - `FLASK_RUN_PORT=8080`

## API Endpoints

|         Endpoint         |  Methods   |            Rule            |
| :----------------------: | :--------: | :------------------------: |
|          static          |    GET     |  /static/<path:filename>   |
| student.create_a_student |    POST    |         /students/         |
|  student.delete_student  |   DELETE   | /students/<int:student_id> |
|  student.get_a_student   |    GET     | /students/<int:student_id> |
|   student.get_students   |    GET     |         /students/         |
|  student.update_student  | PATCH, PUT | /students/<int:student_id> |
| teacher.create_a_teacher |    POST    |         /teachers/         |
|  teacher.delete_teacher  |   DELETE   | /teachers/<int:teacher_id> |
|  teacher.get_a_teacher   |    GET     | /teachers/<int:teacher_id> |
|   teacher.get_teachers   |    GET     |         /teachers/         |
|  teacher.update_teacher  | PATCH, PUT | /teachers/<int:teacher_id> |
