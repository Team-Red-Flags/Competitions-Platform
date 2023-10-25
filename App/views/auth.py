from datetime import date
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    jwt_authenticate,
    authenticate_admin,
    authenticate_student,
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
    
    
@auth_views.route('/signup', methods=['POST'])
def signup_action():
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    print("Signup received")
    if create_student(
        username=data['username'],
        password=data['password'],
        fname=data['fname'],
        lname=data['lname'],
        student_id=data['student_id'],
        student_email=data['student_email'],
        dob=date(
            year=int(data['dob'].split('-')[0]), 
            month=int(data['dob'].split('-')[1]), 
            day=int(data['dob'].split('-')[2])
        ),
        image=data['image']
    ): return jsonify(message=f'Student {data["fname"]} {data["lname"]} created'), 200
    return jsonify(message='Failed to create student'), 400


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
@auth_views.route('/student/login', methods=['POST'])
def user_login_action():
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    print("Student login received: " + f"[{data['username']}, {data['password']}]")
    student = authenticate_student(data['username'], data['password'])
    if not student: return jsonify(error='bad username or password given'), 401
    login_user(student)
    return jsonify(message=f'Student {student.fname} {student.lname} logged in!'), 200