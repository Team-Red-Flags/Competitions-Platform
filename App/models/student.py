from datetime import date
from App.database import db
from App.models import User
from sqlalchemy import Column, ForeignKey, Integer, String, Date, LargeBinary
from sqlalchemy.orm import relationship

class Student(User):
    __tablename__ = 'student'
    user = relationship('User', back_populates='student')
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    student_id = Column(Integer, nullable=False, unique=True)
    student_email = Column(String(80), nullable=False, unique=False)
    dob =  Column(Date, nullable=False)
    image = Column(LargeBinary, nullable=True, unique=False)
    
    
    def __init__(self, 
                 username: str, 
                 password: str, 
                 fname: str, 
                 lname: str, 
                 student_id: int, 
                 student_email: str, 
                 dob: date,
                 image: bytes = None):
        """Constructor for a student type user. Inherits from base class User

        Args:
            username (str): _description_
            password (str): _description_
            fname (str): _description_
            lname (str): _description_
            student_id (int): _description_
            student_email (str): _description_
            dob (date): _description_
            image (bytes, optional): _description_. Defaults to None.
        """
        super().__init__(username, password)
        super().set_user_type('student')
        self.fname = fname
        self.lname = lname
        self.student_id = student_id
        self.student_email = student_email
        self.dob = dob
        self.image = image
        
        
    def get_json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "student_id": self.student_id,
            "fname" : self.fname,
            "lname" : self.lname,
            "student_email" : self.student_email,
            "dob" : self.dob 
        }
        
        
    def __str__(self):
        """String representation of the student object

        Returns:
            str: A prettified string representation of the student object
        """
        return f"<Student {self.id}: {self.username}>"
