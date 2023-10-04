from App.models import Competition

def create_competition() -> Competition:
    return None

def get_competition(id) -> Competition:
    return Competition.query.get(id)

def get_all_competitions() -> list:
    return Competition.query.all()

def get_competition_participants(id):
    return None

def update_competition_results():
    return None