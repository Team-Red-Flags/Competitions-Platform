from App.database import db
from App.models import User, Competition
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship

class Participant(db.Model):
    __tablename__ = "participant"
    id             = Column(Integer, primary_key=True)
    participant    = relationship('User')
    competition    = relationship('Competition')
    participant_id = Column(Integer, db.ForeignKey('user.id'))
    competition_id = Column(Integer, db.ForeignKey('competition.id'))
    start_date     = Column(Date, nullable=False, default=now())
    end_date       = Column(Date, nullable=True)
    
    
    def __init__(self, participant: User, competition: Competition):
        self.participant_id = participant.id
        self.competition_id = competition.id


    def get_json(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'competition_id': self.competition_id
        }