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
    users = get_all_students()
    if not users: return []
    return [user.get_json() for user in users]

def update_student(id, username) -> Student:
    user = get_student(id)
    user.username = username
    db.session.add(user)
    db.session.commit()
    return user