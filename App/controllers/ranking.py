from App.database import db
from App.models import Ranking

def create_rank(rank: int, participant_id: int) -> Ranking:
    new_rank = Ranking(rank, participant_id)
    db.session.add(new_rank)
    db.session.commit()
    print("Created new rank:", new_rank)
    return new_rank

def update_rankings(rank):
    return None