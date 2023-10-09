from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_competition,
    ranking_participants,
    create_competition,
    get_all_competitions,
    create_score,
    get_score,
    update_score,
    is_participant
)

competition_views = Blueprint('competition_views', __name__, template_folder='../templates')

@competition_views.route('/competition/create', methods=['POST'])
@login_required
def create_competition_action():
    if not current_user.is_admin(): return jsonify(error='Not an admin'), 403
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    if not data: return jsonify(error='No competition data given'), 400
    name, desc = data['name'], data['description']
    start_date = data['start_date'] if data.__contains__('start_date') else None
    end_date = data['end_date'] if data.__contains__('end_date') else None
    
    # Check that competition name does not already exist
    for comp in get_all_competitions():
        if comp.name == name: 
            return jsonify(error='Competition name already exists'), 400
    
    new_competition = create_competition(name, desc, start_date)
    return jsonify(message='Competition created'), 200
    

@competition_views.route('/competition/add-result', methods=['POST'])
@login_required
def create_results_action():
    if not current_user.is_admin(): return jsonify(error='Not an admin'), 403
    
    # Get data from the request
    form_data = request.form if request.form else None
    data = request.json if request.json else form_data
    if not data: return jsonify(error='No results data given'), 400
    competition_id, participant_id, score =  data['competition_id'], data['participant_id'], data['score']
    
    # Find the participant
    if not is_participant(participant_id):
        return jsonify(error=f'Participant id {participant_id} does not exist'), 400
    
    # Check if existing score already exists. Create if not else update
    score = get_score(participant_id, competition_id)
    if not score:
        create_score(participant_id, competition_id, score)
        return jsonify(message='Added new result'), 200
    
    if update_score(participant_id, competition_id, score):
        return jsonify(message='Successfully updated result'), 200
    
    return jsonify(error='Could not add result'), 400

@competition_views.route('/competition/<int:competition_id>', methods=['GET'])
@login_required
def view_details(competition_id):
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404

    return jsonify(get_competition(competition_id).get_json()), 200


@competition_views.route('/competition/<int:competition_id>/rankings', methods=['GET'])
@login_required
def view_rankings(competition_id):
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404
    rankings_json = [rank.get_json() for rank in ranking_participants(competition_id)]
    return jsonify(rankings_json), 200