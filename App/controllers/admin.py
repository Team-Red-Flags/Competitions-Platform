from App.models import Admin
from App.database import db

def create_admin(username, password) -> Admin:
    newadmin = Admin(username=username, password=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_admin_by_username(username) -> Admin:
    return Admin.query.filter_by(username=username).first()

def get_admin(id) -> Admin:
    return Admin.query.get(id)