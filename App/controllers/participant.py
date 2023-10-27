from App.models import Participant, Competition
from App.database import db

def create_participant(user_id: int, competition_id: int) -> Participant:
    new_participant = Participant(user_id, competition_id)
    db.session.add(new_participant)
    db.session.commit()
    print("Added participant:", new_participant)
    return new_participant

def is_participant(user_id, competition_id) -> bool:
    return Participant.query.filter_by(
        user_id = user_id,
        competition_id = competition_id
    ).first() != None

def get_participant(user_id, competition_id) -> Participant:
    return Participant.query.filter_by(
        user_id = user_id,
        competition_id = competition_id
    ).first()

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

def get_all_participants_json() -> dict:
    parts = {}
    part_list = [participant.get_json() for participant in get_all_participants()]
    if not part_list: return []
    for part in part_list: parts[part['id']] = part
    return parts

def get_participant_competitions(user_id) -> dict:
    comps = {}
    results = Participant.query.filter_by(user_id = user_id).all()
    if not results: return {}
    comps_list = [Competition.query.get(comp.id) for comp in results]
    for comp in comps_list: comps[comp['competition_id']] = comp
    return comps

def get_participant_competition_scores(user_id) -> dict:
    comps = {}
    results = Participant.query.filter_by(user_id = user_id).all()
    if not results: return {}
    comps_list = [comp.get_json() for comp in results]
    for comp in comps_list: comps[comp['competition_id']] = comp
    return comps

def get_competition_rankings(competition_id) -> list:
    records = Participant.query.filter_by(competition_id = competition_id).all()
    if not records: return []
    results_json = [record.get_json() for record in records]
    
    # Sort results_json object by score key in descending order
    return sorted(results_json, key = lambda x: x['score'], reverse = True)

def get_top_20_participants(competition_id) -> list:
    return get_competition_rankings(competition_id)[:20]

def delete_participant(user_id, competition_id) -> bool:
    try:
        participant = get_participant(user_id, competition_id)
        db.session.delete(participant)
        db.session.commit()
        return True
    
    except Exception as e:
        print(e)
        return False