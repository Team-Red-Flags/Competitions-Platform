from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required
)

competition_views = Blueprint('competition_views', __name__, template_folder='../templates') #unsure of use& relevance


@competition_views.route('/competition/create')
@login_required
def create_competition(): pass


@competition_views.route('/competition/update')
@login_required
def update_competition(): pass


@competition_views.route('/competition/view/<int:id>', methods=['POST'])
@login_required
def view_competition(id: int):
    return 'Competition Joined'


@competition_views.route('/competition/')
@login_required
def view_compeition_results(): pass
