from App.database import db
from App.models import User
from sqlalchemy import Column, ForeignKey, Integer, String, Date, LargeBinary
from sqlalchemy.orm import relationship

class Student(User):
    __tablename__ = 'student'
    user = relationship('User')
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    student_id = Column(Integer)
    student_email = Column(String(80), nullable=False)
    dob =  Column(Date, nullable=False)
    image = Column(LargeBinary, nullable=False, unique=False)
    
    
    def __init__(self, username: str, password: str):
        """Constructor for a student type user. Inherits from base class User

        Args:
            username (str): The username of the user
            password (str): The plaintext password of the user. Will be hashed
        """
        super().__init__(username, password)
        super().set_user_type('student')
        
        
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
