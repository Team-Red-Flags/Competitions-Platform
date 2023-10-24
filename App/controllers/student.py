from App.models import Student
from App.database import db

def create_student(username, password) -> Student:
    new_student = Student(username=username, password=password)
    db.session.add(new_student)
    db.session.commit()
    print("Created user:", new_student)
    return new_student

def get_student_by_username(username) -> Student:
    return Student.query.filter_by(username=username).first()

def get_student(id) -> Student:
    return Student.query.get(id)

def get_all_students() -> list:
    return Student.query.all()

def get_all_students_json() -> list:
    students = get_all_students()
    if not students: return []
    return [student.get_json() for student in students]

def update_student(id, username) -> Student:
    student = get_student(id)
    student.username = username
    db.session.add(student)
    db.session.commit()
    return student