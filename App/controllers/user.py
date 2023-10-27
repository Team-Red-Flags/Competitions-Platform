from App.models import User, Student, Admin
from App.database import db

def create_user(username, password) -> User:
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    print("Created user:", new_user)
    return new_user

def get_user_by_username(username) -> User:
    return User.query.filter_by(username=username).first()

def get_user(id) -> User:
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json() -> dict:
    users = {}
    users_list = [user.get_json() for user in get_all_users()]
    if not users_list: return {}
    for user in users_list: users[user['id']] = user
    return users

def update_user(id, username) -> User:
    user = get_user(id)
    user.username = username
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(id) -> bool:
    try:
        user = get_user(id)
        db.session.delete(user)
        db.session.commit()
        return True
    
    except Exception as e:
        print(e)
        return False