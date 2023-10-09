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
    
    
    def __init__(self, participant: User, competition: Competition):
        self.participant_id = participant.id
        self.competition_id = competition.id


    def get_json(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'competition_id': self.competition_id
        }
        
    
    def __str__(self):
        return f"<Participant {self.id}: {User.query.get(self.participant_id).username}, {Competition.query.get(self.competition_id).name}>"
    
    
    def __repr__(self):
        return self.__str__()