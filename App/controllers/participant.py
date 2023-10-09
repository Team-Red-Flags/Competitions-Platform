from App.models import Participant, Competition
from App.database import db

def create_participant(user_id: int, competition_id: int) -> Participant:
    new_participant = Participant(user_id, competition_id)
    db.session.add(new_participant)
    db.session.commit()
    print("Added new participant:", new_participant)
    return new_participant

def is_participant(user_id) -> bool:
    return Participant.query.filter_by(user_id=user_id).first() != None

def update_participant_score(user_id, competition_id, score) -> bool:
    participant = Participant.query.filter_by(
        user_id = user_id, 
        competition_id = competition_id
    ).first()
    if not participant: return False
    participant.score = score
    db.session.add(participant)
    db.session.commit()
    return True

def get_all_participants():
    return Participant.query.all()

def get_all_participants_json() -> list:
    participants = get_all_participants()
    if not participants: return []
    return [participant.get_json() for participant in participants]

def get_participant_competitions(user_id) -> list:
    results = Participant.query.filter_by(user_id = user_id).all()
    if not results: return []
    return [Competition.query.get(result.competition_id) for result in results]

def get_competition_rankings(competition_id) -> list:
    records = Participant.query.filter_by(competition_id = competition_id).all()
    if not records: return []
    results_json = [record.get_json() for record in records]
    
    # Sort results_json object by score key in descending order
    results_json = sorted(results_json, key=lambda x: x['score'], reverse=True)
    print(results_json)
    return results_json