from App.models import Participant, User, Competition
from App.database import db

def create_participant(participant: User, competition: Competition):
    new_participant = Participant(participant, competition)
    db.session.add(new_participant)
    db.session.commit()
    print("Added new participant:", new_participant)
    return participant

def get_all_participants():
    return Participant.query.all()

def get_participant_competitions(participant_id) -> list:
    results = Participant.query.filter_by(participant_id=participant_id).all()
    if not results: return []
    return [Competition.query.get(result.competition_id).get_json() for result in results]

def get_all_participants_json() -> list:
    participants = get_all_participants()
    if not participants: return []
    return [participant.get_json() for participant in participants]
