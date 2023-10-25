from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from json import load
from os import path
from base64 import b64encode
from datetime import date
from App.models import db
from App.controllers import (
    create_student, 
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
    img = b64encode(open(path.join(path.dirname(__file__).split('App')[0] + 'images/user.png'), 'rb').read())
    
    # Create users
    bob = create_student(
        username='bob', 
        password='bobpass', 
        fname='Bob', 
        lname='the Builder', 
        student_id=80012345, 
        student_email='bob.thebuilder@my.uwi.edu',
        dob = date(2000, 1, 1),
        image=img
    )
    
    rob = create_student(
        username='rob',
        password='robpass',
        fname='Rob',
        lname='Robinson',
        student_id=80012346,
        student_email='rob.robinson@my.uwi.edu',
        dob = date(1998, 1, 4),
        image=img
    )
    
    ben = create_student(
        username='ben',
        password='benpass',
        fname='Ben',
        lname='Simpson',
        student_id=80012347,
        student_email='ben.simpson@my.uwi.edu',
        dob = date(1999, 5, 11),
        image=img
    )
    
    # Create admin
    lily = create_admin(
        username='lily', 
        password='lilypass',
        fname='Lily',
        lname='Potter',
        image=img
    )
    
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