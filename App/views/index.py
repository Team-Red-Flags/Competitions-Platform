from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user, create_admin

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@index_views.route('/init', methods=['GET'])
def init():
    """
    This method initializes the database. Should ONLY be called by a logged-in administrator. 
    Implement verification before deploying.
    """
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_admin('lily', 'lilypass')
    print('Database intialised to default state')
    return jsonify(message='db initialised!')


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})