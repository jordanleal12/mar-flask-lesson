from .cli_controller import db_commands
from .student_controller import student_bp
from .teacher_controller import teacher_bp

controller_blueprints = [db_commands, student_bp, teacher_bp]
