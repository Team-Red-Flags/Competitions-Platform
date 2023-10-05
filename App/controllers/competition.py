from App.database import db
from App.models import Competition
from datetime import datetime

def create_competition(name: str, description: str, start_date: str = None, end_date: str = None) -> Competition:
    start_date = datetime.strptime(start_date, '%d %B, %Y') if start_date else None
    end_date = datetime.strptime(end_date, '%d %B, %Y') if end_date else None
    new_competition = Competition(name, description, start_date, end_date)
    db.session.add(new_competition)
    db.session.commit()
    print("Created new competition: " + f"[{name}, {description}, {start_date}, {end_date}]")
    return new_competition

def get_competition(id) -> Competition:
    return Competition.query.get(id)

def get_all_competitions() -> list[Competition]:
    return Competition.query.all()

def add_competition_participant(competition_id, participant_id):
    return None

def get_competition_participants(competition_id):
    return None

def update_competition_results(competition_id):
    return None