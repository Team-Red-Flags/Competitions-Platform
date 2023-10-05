from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from sqlalchemy import Column, Integer, String

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id       = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    type     = Column(String, nullable=False, default='user')
    

    def __init__(self, username, password, type='user'):
        self.username = username
        self.set_password(password, 'scrypt')
        self.type = type if type in ['user', 'admin'] else 'user'


    def get_json(self) -> dict[str]:
        return {
            'id': self.id,
            'username': self.username
        }
        
        
    def is_admin(self) -> bool:
        """Checks if the user is an admin.

        Returns:
            bool: True if the user is an admin. False otherwise
        """
        return self.type == 'admin'
    

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
        return f"<{self.type.capitalize()} {self.id}: {self.username}>"
    
    
    def __repr__(self):
        """Calls the __str__ method to represent the user
        """
        return self.__str__()
