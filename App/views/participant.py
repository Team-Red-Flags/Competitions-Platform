from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_competition,
    get_participant_competitions,
    create_participant
)

participant_views = Blueprint('participant_views', __name__, template_folder='../templates')


@participant_views.route('/enroll/<int:user_id>/<int:competition_id>', methods=['POST'])
@login_required
def enroll_participant(user_id, competition_id):
    if not current_user.is_admin(): return jsonify(error='Not an admin'), 403
    competitions = get_participant_competitions(user_id)
    for competition in competitions:
        if competition.id == competition_id: 
            return jsonify(error=f'User {user_id} already enrolled in this competition'), 400
    if create_participant(user_id, competition_id):
        return jsonify(message=f"Enrolled user {user_id} to {get_competition(competition_id).name}"), 200
    return jsonify(error=f"Failed to enroll user {user_id} to {get_competition(competition_id).name}"), 400