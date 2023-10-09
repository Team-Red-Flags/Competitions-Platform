from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_user,
    get_competition,
    ranking_participants,
    create_competition,
    get_all_competitions
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
    

@competition_views.route('/competition/update')
@login_required
def update_competition_results():
    
    # Authenticate admin to proceed
    
    # Fetch data to update competition scores (competition id, participant id, score)
    
    # Update the rankings

    return jsonify(message='Competition results updated'), 200


@competition_views.route('/competition/<int:competition_id>/view-rankings', methods=['GET'])
@login_required
def view_rankings(competition_id):
    if not get_competition(competition_id):
        return jsonify(error=f'Competition with id {competition_id} not found'), 404
    rankings_json = [rank.get_json() for rank in ranking_participants(competition_id)]
    return jsonify(rankings_json), 200