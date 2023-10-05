from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    login_admin,
    login_user,
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
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/logout', methods=['GET'])
@login_required
def logout_action():
    curr_user = current_user
    logout_user()
    return jsonify(f'{curr_user.username} logged out!')


'''
Admin Routes
'''

@auth_views.route('/admin/login', methods=['POST'])
def admin_login_action():
    data = request.form
    admin = login_admin(data['username'], data['password'])
    if not admin: return 'bad username or password given', 401
    login_user(admin)
    return jsonify(f'{admin.username} logged in!')


'''
User Routes
'''

@auth_views.route('/user/login', methods=['POST'])
def user_login_action():
    data = request.form
    user = login_user(data['username'], data['password'])
    if not user: return 'bad username or password given', 401
    login_user(user)
    return jsonify(f'{user.username} logged in!')


'''
Redirects
'''
@auth_views.route('/login', methods=['GET'])
def default_login_action():
    return redirect(url_for('auth_views.user_login_action'))