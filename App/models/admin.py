from App.database import db
from App.models import User

class Admin(User):
    
    def __init__(self, username: str, password: str):
        """Constructor for an admin type user. Inherits from base class User

        Args:
            username (str): The username of the user
            password (str): The plaintext password of the user. Will be hashed
        """
        super().__init__(username, password)
        super().set_user_type('admin')
