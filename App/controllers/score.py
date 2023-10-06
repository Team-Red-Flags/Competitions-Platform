from App.database import db
from App.models import Score

def create_score(participant_id: int, competition_id: int, score: int) -> Score:
    new_score = Score(participant_id, competition_id, score)
    db.session.add(new_score)
    db.session.commit()
    print("Created new score:", new_score)
    return new_score

def ranking_participants(competition_id):
    all_scores = Score.query.filter_by(competition_id=competition_id)
    return all_scores.sort(key=lambda x: x.score, reverse = True)