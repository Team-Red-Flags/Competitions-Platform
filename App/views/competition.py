from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    get_competition,
    get_competition_rankings,
    create_competition,
    get_all_competitions,
    get_user,
    get_admin,
    update_participant_score,
    is_participant,
    delete_competition
)

competition_views = Blueprint('competition_views', __name__, template_folder='../templates')

@competition_views.route('/competition/create', methods=['POST'])
@login_required
def create_competition_action():
    
    # Authenticate admin
    if not get_admin(current_user.id): return jsonify(error='Not an admin'), 403
    
    # Get data from the request
    form_data = request.form if request.form else None
    data = request.json if not form_data else form_data
    if not data: return jsonify(error='No competition data given'), 400
    name, desc = data['name'], data['description']
    start_date = data['start_date'] if data.__contains__('start_date') else None
    end_date = data['end_date'] if data.__contains__('end_date') else None
    
    # Check that competition name does not already exist
    for comp in get_all_competitions():
        if comp.name == name: 
            return jsonify(error='Competition name already exists'), 400
    
    competition = create_competition(name, desc, start_date)
    return jsonify(competition.get_json()), 200
    

@competition_views.route('/competition/add-result', methods=['POST'])
@login_required
def add_results_action():
    
    # Authenticate admin
    if not get_admin(current_user.id): return jsonify(error='Not an admin'), 403
    
    # Get data from the request
    form_data = request.form if request.form else None
    data = request.json if not form_data else form_data
    if not data: return jsonify(error='No results data given'), 400
    competition_id, user_id, score =  data['competition_id'], data['user_id'], data['score']
    print(f"Adding result for user {user_id} in competition {competition_id}: {score}")
    
    # Verify user id
    if not get_user(user_id):
        return jsonify(error=f'User id {user_id} does not exist'), 400
    
    # Verify existing competition
    if not get_competition(competition_id):
        return jsonify(error=f'Competition id {competition_id} does not exist'), 400
    
    # Find the participant
    if not is_participant(user_id, competition_id):
        return jsonify(error=f'User id {user_id} not a participant of competition {competition_id}'), 400
    
    # Update participant score
    if update_participant_score(user_id, competition_id, score):
        print("Record updated")
        return jsonify(message='Successfully updated result'), 200
    
    print("Could not add result")
    return jsonify(error='Could not add result'), 400

@competition_views.route('/competition/<int:competition_id>', methods=['GET'])
def view_details(competition_id):
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404

    return jsonify(get_competition(competition_id).get_json()), 200


@competition_views.route('/competition/<int:competition_id>/rankings', methods=['GET'])
def view_rankings(competition_id):
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404
    return jsonify(get_competition_rankings(competition_id)), 200


@competition_views.route('/competition/delete/<int:competition_id>', methods=['DELETE'])
@login_required
def delete_competition_action(competition_id):
    
    # Authenticate admin
    if not get_admin(current_user.id): return jsonify(error='Not an admin'), 403
    
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404
    
    if not delete_competition(competition_id):
        return jsonify(error='Failed to delete competition'), 400
    
    return jsonify(message='Competition successfully deleted'), 200