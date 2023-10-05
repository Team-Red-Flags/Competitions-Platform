from App.database import db
from App.models import Competition
from datetime import date

def create_competition(name: str, description: str, start_date: date = None, end_date: date = None) -> Competition:
    new_competition = Competition(name, description, start_date, end_date)
    db.session.add(new_competition)
    db.session.commit()
    print("Created new competition: " + f"[{name}, {description}, {start_date}, {end_date}]")
    return new_competition

def get_competition(id) -> Competition:
    return Competition.query.get(id)

def get_all_competitions() -> list:
    return Competition.query.all()

def add_competition_participant(competition_id, participant_id):
    return None

def get_competition_participants(competition_id):
    return None

def update_competition_results(competition_id):
    return None