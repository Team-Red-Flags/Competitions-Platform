from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import User

def jwt_authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password): return None 
    return create_access_token(identity=username)

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password): return None
    return user

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if not user: return None
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return User.query.get(jwt_data["sub"])

    return jwt