from App.database import db
from App.models import User

class Admin(User):
    
    def __init__(self, username, password):
        super().__init__(username, password, type='admin')
