from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from json import load
from App.models import db
from App.controllers import (
    create_user, 
    create_admin,
    create_competition,
    create_participant
)

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
    
    # Create users
    create_user('bob', 'bobpass')
    rob = create_user('rob', 'robpass')
    ben = create_user('ben', 'benpass')
    create_admin('lily', 'lilypass')
    
    # Create competitions
    with open('App/static/competitions.json', 'r') as f:
        competitions = load(f)
        for comp in competitions:
            create_competition(
                comp['name'], 
                comp['description'], 
                comp['start_date'], 
                comp['end_date']
            )
            
    # Create participants
    create_participant(rob.id, 1)
    create_participant(ben.id, 3)
    return jsonify(message='db initialised!')


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'}), 200