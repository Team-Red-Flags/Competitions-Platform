from App.database import db
from sqlalchemy import Column, Integer
from sqlalchemy.sql.functions import now
from App.models import Participant
from sqlalchemy.orm import relationship

class Score (db.Model):
    __tablename__ = "score"
    id          = Column(Integer, primary_key=True, nullable=False)
    participant    = relationship('Participant')
    competition = relationship('Competition')
    participant_id = Column(Integer, db.ForeignKey('participant.id'))
    competition_id = Column(Integer, db.ForeignKey('competition.id'))
    score        = Column(Integer, nullable=False)
    

    def __init__(self, participant_id, competition_id, score):
        self.participant_id = participant_id
        self.competition_id = competition_id
        self.score = score
        
        
    def get_json(self):
        return {
            'competition id': self.competition_id,
            'participant id': self.participant_id,
            'score': self.score
        }
    
        