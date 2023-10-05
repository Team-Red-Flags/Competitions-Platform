from App.models import Participant, User, Competition
from App.database import db

def create_participant(participant: User, competition: Competition):
    new_participant = Participant(participant, competition)
    db.session.add(new_participant)
    db.session.commit()
    print("Added new participant: " + f"[{participant.username}, {competition.name}]")
    return participant

def get_participant(id) -> Participant:
    return Participant.query.get(id)

def get_all_participants():
    return Participant.query.all()

def get_competition_participants(competition_id):
    return Participant.query.get(competition_id)

def get_all_participants_json() -> list[dict]:
    participants = get_all_participants()
    if not participants: return []
    return [participant.get_json() for participant in participants]
