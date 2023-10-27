from App.database import db
from App.models import User
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

class Admin(User):
    __tablename__ = 'admin'
    user = relationship('User', back_populates='user')
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    image = Column(LargeBinary, nullable=True, unique=False)
    
    
    def __init__(self, username: str, password: str, fname: str, lname: str, image: bytes = None):
        """Constructor for an admin type user. Inherits from base class User

        Args:
            username (str): The username of the user
            password (str): The plaintext password of the user. Will be hashed
        """
        super().__init__(username, password)
        super().set_user_type('admin')
        self.fname = fname
        self.lname = lname
        self.image = image
        
        
    def get_json(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'fname' : self.fname,
            'lname' : self.lname        
        }


    def is_admin(self) -> bool:
        """Overrides base class method to return True

        Returns:
            bool: True for all instances of Admin
        """
        return True
    
    
    def __str__(self):
        """String representation of the admin object

        Returns:
            str: A prettified string representation of the admin object
        """
        return f"<Admin {self.id}: {self.username}>"