from App.models import Competition

def create_competition() -> Competition:
    return None

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