from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_user,
    get_competition,
    create_participant
)

participant_views = Blueprint('participant_views', __name__, template_folder='../templates')


@participant_views.route('/enroll/<int:participant_id>/<int:competition_id>', methods=['POST'])
@login_required
def enroll_participant(participant_id, competition_id):
    print(current_user)
    if not current_user.is_admin(): return jsonify(error='Not an admin'), 403
    user, competition = get_user(participant_id), get_competition(competition_id)
    if create_participant(user, competition):
        return jsonify(f"Added {user.username} to {competition.name}"), 200
    return jsonify(f"Failed to add {user.username} to {competition.name}"), 400