from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import get_participant_competitions

user_views = Blueprint('user_views', __name__, template_folder='../templates')

#view profile
@user_views.route('/profile', methods=['GET'])
@login_required
def view_profile():
    return