from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_user,
    get_admin,
    is_participant,
    get_competition,
    delete_participant,
    get_participant_competitions,
    create_participant
)

participant_views = Blueprint('participant_views', __name__, template_folder='../templates')


@participant_views.route('/enroll/<int:user_id>/<int:competition_id>', methods=['POST'])
@login_required
def enroll_participant(user_id, competition_id):
    
    # Authenticate admin
    if not get_admin(current_user.id): return jsonify(error='Not an admin'), 403
    
    # Verify existing user
    if not get_user(user_id):
        return jsonify(error=f'User id {user_id} does not exist'), 400
    
    # Verify existing competition
    if not get_competition(competition_id):
        return jsonify(error=f'Competition {competition_id} does not exist'), 400
    
    # Verify user is not already enrolled
    competitions = get_participant_competitions(user_id)
    for k, v in competitions.items():
        if k == competition_id:
            return jsonify(error=f'User {user_id} already enrolled into competition {competition_id}'), 400
        
    # Enroll user to competition
    if create_participant(user_id, competition_id):
        return jsonify(message=f"Enrolled user {user_id} to competition {competition_id}"), 200
    
    return jsonify(error=f"Failed to enroll user {user_id} to competition {competition_id}"), 400


@participant_views.route('/unenroll/<int:user_id>/<int:competition_id>', methods=['POST'])
@login_required
def unenroll_participant(user_id, competition_id):
    
    # Authenticate admin
    if not get_admin(current_user.id): return jsonify(error='Not an admin'), 403
    
    # Verify existing user
    if not get_user(user_id):
        return jsonify(error=f'User id {user_id} does not exist'), 400
    
    # Verify existing competition
    if not get_competition(competition_id):
        return jsonify(error=f'Competition id {competition_id} does not exist'), 400
    
    # Verify user is already enrolled
    if not is_participant(user_id, competition_id):
        return jsonify(error=f'User {user_id} not enrolled in this competition'), 400
    
    # Unenroll user from competition
    if delete_participant(user_id, competition_id):
        return jsonify(message=f"Unenrolled user {user_id} from {get_competition(competition_id).name}"), 200
    
    return jsonify(error=f"Failed to unenroll user {user_id} from {get_competition(competition_id).name}"), 400