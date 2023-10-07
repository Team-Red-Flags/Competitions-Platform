from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    authenticate_admin,
    authenticate_user,
    get_user,
    get_all_users,
    get_all_users_json
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({
        'message': f"username: {current_user.username}", 
        'id' : f"{current_user.id}"
        }), 200


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return jsonify(message=f'User logged out!'), 200


'''
Admin Routes
'''

@auth_views.route('/admin/login', methods=['POST'])
def admin_login_action():
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    print("Admin login received: " + f"[{data['username']}, {data['password']}]")
    admin = authenticate_admin(data['username'], data['password'])    
    if not admin: return jsonify(error='bad username or password given'), 401
    login_user(admin)
    return jsonify(message=f'Admin {admin.username} logged in!'), 200


'''
User Routes
'''

@auth_views.route('/login', methods=['POST'])
@auth_views.route('/user/login', methods=['POST'])
def user_login_action():
    data = request.form if request.form else None
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    print("User login received: " + f"[{data['username']}, {data['password']}]")
    user = authenticate_user(data['username'], data['password'])
    if not user: return jsonify(error='bad username or password given'), 401
    login_user(user)
    return jsonify(message=f'User {user.username} logged in!'), 200