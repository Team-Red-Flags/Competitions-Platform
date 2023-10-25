from App.models import Student
from App.database import db

def create_student(
        username: str, 
        password: str, 
        fname: str, 
        lname: str, 
        student_id: int, 
        student_email: str, 
        dob, 
        image: bytes = None
        ) -> Student:
    
    new_student = Student(
        username=username, 
        password=password,
        fname=fname,
        lname=lname,
        student_id=student_id,
        student_email=student_email,
        dob=dob,
        image=image
    )
    db.session.add(new_student)
    db.session.commit()
    print("Created student:", new_student)
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

def update_student(
    id, 
    username, 
    password = None, 
    fname = None, 
    lname = None, 
    student_id = None, 
    student_email = None, 
    dob = None,
    image = None
    ) -> Student:
    
    student = get_student(id)
    student.username = username
    student.fname = fname if fname else student.fname
    student.lname = lname if lname else student.lname
    student.student_id = student_id if student_id else student.student_id
    student.student_email = student_email if student_email else student.student_email
    student.dob = dob if dob else student.dob
    student.image = image if image else student.image
    if password: student.set_password(password)
    db.session.add(student)
    db.session.commit()
    return student