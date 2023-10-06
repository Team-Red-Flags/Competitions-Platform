from App.database import db
from sqlalchemy import Column, Integer
from sqlalchemy.sql.functions import now
from App.models import Participant
from sqlalchemy.orm import relationship

class Score (db.Model):
    __tablename__ = "score"
    rank        = Column(Integer, primary_key=True, nullable=False)
    participant    = relationship('Participant')
    participant_id = Column(Integer, db.ForeignKey('participant.id'))
    

    def __init__(self, rank, participant_id):
        self.rank        = rank
        self.participant_id = participant_id
        
        
    def get_json(self):
        return {
            'rank': self.rank,
            'participant id': self.participant_id,
        }
        