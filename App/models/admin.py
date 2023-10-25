from App.database import db
from App.models import User
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Admin(User):
    __tablename__ = 'admin'
    user = relationship('User')
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    
    
    def __init__(self, username: str, password: str):
        """Constructor for an admin type user. Inherits from base class User

        Args:
            username (str): The username of the user
            password (str): The plaintext password of the user. Will be hashed
        """
        super().__init__(username, password)
        super().set_user_type('admin')


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