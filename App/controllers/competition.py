from App.utils import get_date_from_string
from App.models import Competition
from App.database import db

def create_competition(name: str, description: str, start_date: str = None, end_date: str = None) -> Competition:
    new_competition = Competition(
        name=name, 
        description=description, 
        start_date=get_date_from_string(start_date), 
        end_date=get_date_from_string(end_date)
    )
    
    try:
        db.session.add(new_competition)
        db.session.commit()
        print("Created competition:", new_competition)
        return new_competition
    
    except Exception as e:
        print(e)
        return None

def get_competition(id) -> Competition:
    return Competition.query.get(id)

def get_competition_by_name(name) -> Competition:
    return Competition.query.filter_by(name=name).first()

def get_all_competitions() -> list:
    return Competition.query.all()

def get_all_competitions_json() -> list:
    return [competition.get_json() for competition in get_all_competitions()]

def update_competition(
        id: int,
        name: str = None, 
        description: str = None, 
        start_date: str = None, 
        end_date: str = None
    ) -> Competition:
    competition = get_competition(id)
    if name: competition.name = name
    if description: competition.description = description
    if start_date: competition.start_date = get_date_from_string(start_date)
    if end_date: competition.end_date = get_date_from_string(end_date)
    db.session.commit()
    return competition

def delete_competition(id) -> bool:
    try:
        competition = get_competition(id)
        db.session.delete(competition)
        db.session.commit()
        return True
    
    except Exception as e:
        print(e)
        return False