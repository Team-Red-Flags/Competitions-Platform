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

competition_views = Blueprint('user_views', __name__, template_folder='../templates') #unsure of use& relevance

#create compet
@competition_views.route('/user', methods=['POST'])
@login_required
def join_compet():
    return 'Competition Joined'

#delete compet
@competition_views.route('/user', methods=['POST'])
@login_required
def leave_compet():
    return 'Competition Left'

#view competition
@competition_views.route('/user', methods=['GET'])
def view_profile():
    return #showProfile()