from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_participant_competitions,
    get_user,
    get_admin,
    get_student,
    update_user,
    update_admin,
    update_student
)

profile_views = Blueprint('profile_views', __name__, template_folder='../templates')


@profile_views.route('/profile', methods=['GET'])
@login_required
def view_profile():
    profile_data = {}
    if get_student(current_user.id): profile_data['user'] = get_student(current_user.id).get_json()
    elif get_admin(current_user.id): profile_data['user'] = get_admin(current_user.id).get_json()
    else: profile_data['user'] = get_user(current_user.id).get_json()
    profile_data['competitions'] =  [comp.get_json() for comp in get_participant_competitions(current_user.id)]
    return jsonify(profile_data), 200


@profile_views.route('/profile', methods=['POST'])
@login_required
def edit_profile():
    form_data = request.form if request.form else None
    data  = request.json if not form_data else form_data
    
    if not update_user(current_user, data['username']):
        return jsonify(error="Username already exists"), 400
    
    try:
        if get_admin(current_user.id):
            update_admin(
                id=current_user.id,
                password=data['password'],
                fname=data['fname'],
                lname=data['lname'],
                image=data['image']
            )
        else: 
            update_student(
                id=current_user.id,
                password=data['password'],
                fname=data['fname'],
                lname=data['lname'],
                dob=data['dob'],
                image=data['image']
            )
    
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    return jsonify(message='Profile updated'), 200