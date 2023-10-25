from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from sqlalchemy import Column, Integer, String

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id       = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    

    def __init__(self, username: str, password: str):
        """Constructor for a user object

        Args:
            username (str): The username of the user
            password (str): The plaintext password of the user. Will be hashed 
        """
        self.username = username
        self.set_password(password)


    def get_json(self) -> dict:
        return {
            'id': self.id,
            'username': self.username
        }
        
        
    def is_admin(self) -> bool:
        """Checks if the user is an admin. Must be overridden by admin subclass instances

        Returns:
            bool: True if the user is an admin. False otherwise
        """
        return False
    
    
    def set_user_type(self, type: str):
        """Sets the user type when inherited by a subclass

        Args:
            type (str): Type of user (student or admin)
        """
        if type.lower() in ['student', 'admin']:
            self.type = type.lower()
        else:
            raise ValueError(f"{type} is not a valid user type")
    

    def set_password(self, password: str, _method: str = 'sha256'):
        """Generates a hashed password for the user using the given method
        (Defaults to sha256)

        Args:
            password (str): The password to be hashed
        """
        self.password = generate_password_hash(password, method=_method)
        
    
    def check_password(self, password: str) -> bool:
        """Checks the given password against the hashed password.

        Args:
            password (str): The password to be checked

        Returns:
            bool: True if the password is correct. False otherwise
        """
        return check_password_hash(self.password, password)
    
    
    def __str__(self):
        """String representation of the user object

        Returns:
            str: A prettified string representation of the user
        """
        return f"<User {self.id}: {self.username}>"
    
    
    def __repr__(self):
        """Calls the __str__ method to represent the user
        """
        return self.__str__()
