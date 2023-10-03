from App.models import Admin
from App.database import db

def create_admin(username, password):
    newuser = Admin(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()

def get_admin(id):
    return Admin.query.get(id)