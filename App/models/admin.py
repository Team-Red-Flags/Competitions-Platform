from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
