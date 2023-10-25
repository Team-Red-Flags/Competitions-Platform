from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_participant_competitions,
    get_user,
    update_student,
    update_admin
)

profile_views = Blueprint('profile_views', __name__, template_folder='../templates')


@profile_views.route('/profile', methods=['GET'])
@login_required
def view_profile():
    profile_data = {}
    profile_data['user'] = current_user.get_json()
    profile_data['competitions'] =  [comp.get_json() for comp in get_participant_competitions(current_user.id)]
    return jsonify(profile_data), 200


@profile_views.route('/profile', methods=['POST'])
@login_required
def edit_profile():
    form_data = request.form if request.form else None
    data  = request.json if not form_data else form_data
    if get_user(current_user.id).is_admin():
        update_admin(
            id=current_user.id,
            username=data['username'],
            password=data['password'],
            fname=data['fname'],
            lname=data['lname'],
            image=data['image']
        )
    else: 
        update_student(
            id=current_user.id,
            username=data['username'],
            password=data['password'],
            fname=data['fname'],
            lname=data['lname'],
            dob=data['dob'],
            image=data['image']
        )
    return jsonify(message='Profile updated'), 200