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
    create_competition,
    get_all_competitions
)

competition_views = Blueprint('competition_views', __name__, template_folder='../templates') #unsure of use& relevance


@competition_views.route('/competition/create', methods=['POST'])
@login_required
def create_competition_action():
    if not current_user.is_admin(): return jsonify(message='Not an admin'), 403
    data = request.form if request.form else None
    if not data: return jsonify(message='No competition data given'), 400
    name, desc = data['name'], data['description']
    start_date = data['start_date'] if data.__contains__('start_date') else None
    end_date = data['end_date'] if data.__contains__('end_date') else None
    
    # Check that competition name does not already exist
    for comp in get_all_competitions():
        if comp.name == name: 
            return jsonify(message='Competition name already exists'), 400
    
    new_competition = create_competition(name, desc, start_date)
    return jsonify(new_competition.get_json()), 200
    

@competition_views.route('/competition/update')
@login_required
def update_competition_action(): pass


@competition_views.route('/competition/view/<int:id>', methods=['POST'])
def view_competition_action(id: int):
    return 'Competition Joined'


@competition_views.route('/competition/')
@login_required
def view_compeition_results(): pass
