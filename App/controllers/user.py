from App.models import User
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username) -> User:
    return User.query.filter_by(username=username).first()

def get_user(id) -> User:
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json() -> list:
    users = get_all_users()
    if not users: return []
    return [user.get_json() for user in users]

def update_user(id, username):
    user = get_user(id)
    if not user: return None
    user.username = username
    db.session.add(user)
    return db.session.commit()
    