from datetime import date
from json import load
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_admin,
    create_student,
    create_competition,
    create_participant
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    img = b64encode(open('App/static/iamges/user.png', 'rb').read())
    
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
    
    print('Database intialised')
