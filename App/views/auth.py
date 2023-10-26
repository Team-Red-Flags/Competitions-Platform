from os import path
from base64 import b64encode
from datetime import date
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    jwt_authenticate,
    authenticate_user,
    create_student
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({
        'message': f"username: {current_user.username}", 
        'id' : f"{current_user.id}"
    }), 200
    
    
@auth_views.route('/register', methods=['POST'])
def register_action():
    form_data = request.form if request.form else None
    data = request.json if not form_data else form_data
    print("Registration received")
    img =  b64encode(request.files['image'].read()) if request.files['image'] else None
    if not img: img = b64encode(open(path.join(path.dirname(__file__).split('App')[0] + 'images/user.png'), 'rb').read())
    if create_student(
        username=data['username'],
        password=data['password'],
        fname=data['fname'],
        lname=data['lname'],
        student_id=data['student_id'],
        student_email=data['student_email'],
        dob=data['dob'],
        image=img
    ): return jsonify(message=f'Student account for {data["fname"]} {data["lname"]} created'), 200
    return jsonify(message='Failed to register student account'), 400


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return jsonify(message=f'User logged out!'), 200


@auth_views.route('/login', methods=['POST'])
@auth_views.route('/admin/login', methods=['POST'])
@auth_views.route('/student/login', methods=['POST'])
def user_login_action():
    form_data = request.form if request.form else None
    data = request.json if not form_data else form_data
    user = authenticate_user(data['username'], data['password'])
    if not user: return jsonify(error='bad username or password given'), 401
    login_user(user)
    
    if user.is_admin():
        print("Admin login received: " + f"[{data['username']}, {data['password']}]")
        return jsonify(message=f'Admin {user.fname} {user.lname} logged in!'), 200
    
    print("Student login received: " + f"[{data['username']}, {data['password']}]")
    return jsonify(message=f'Student {user.fname} {user.lname} logged in!'), 200