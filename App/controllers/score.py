from App.database import db
from App.models import Score

def create_score(participant_id: int, competition_id: int, score: int) -> Score:
    new_score = Score(participant_id, competition_id, score)
    db.session.add(new_score)
    db.session.commit()
    print("Created new score:", new_score)
    return new_score

def get_all_scores():
    return Score.query.all()

#ranks all participants for a particular competition
def ranking_participants(competition_id):
    all_scores = Score.query.filter_by(competition_id=competition_id)
    return all_scores.sort(key=lambda x: x.score, reverse = True)
        
#gets participant rank for a particular competition
def get_rank(competition_id, participant_id):
    ranked_participants = ranking_participants(competition_id)
    for participant in ranked_participants:
        count+= 1
        if participant.participant_id == participant_id:
            return count
    return -1

#determines if participant is in top 20 for a particular competition
def top_20(competition_id, participant_id):
    rank = get_rank(competition_id, participant_id)

    if rank <= 20:
        return True
    else:
        return False 