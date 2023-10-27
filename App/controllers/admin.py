from App.models import Admin
from App.database import db

def create_admin(username, password, fname, lname, image: bytes = None) -> Admin:
    new_admin = Admin(
        username=username, 
        password=password,
        fname=fname,
        lname=lname,
        image=image
    )
    db.session.add(new_admin)
    db.session.commit()
    print("Created admin:", new_admin)
    return new_admin

def get_admin_by_username(username) -> Admin:
    return Admin.query.filter_by(username=username).first()

def get_admin(id) -> Admin:
    return Admin.query.get(id)

def get_all_admins() -> list:
    return Admin.query.all()

def get_all_admins_json() -> list:
    admins = get_all_admins()
    if not admins: return []
    return [admin.get_json() for admin in admins]

def update_admin(id, password = None, fname = None, lname = None, image = None) -> Admin:
    admin = get_admin(id)
    admin.fname = fname if fname else admin.fname
    admin.lname = lname if lname else admin.lname
    admin.image = image if image else admin.image
    if password: admin.set_password(password) 
    db.session.add(admin)
    db.session.commit()
    return admin

def delete_admin(id) -> bool:
    try:
        admin = get_admin(id)
        db.session.delete(admin)
        db.session.commit()
        return True
    
    except Exception as e:
        print(e)
        return False