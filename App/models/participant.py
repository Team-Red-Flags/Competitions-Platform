from App.database import db
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

class Participant(db.Model):
    __tablename__ = "participant"
    id             = Column(Integer, primary_key=True)
    participant    = relationship('User')
    competition    = relationship('Competition')
    user_id        = Column(Integer, db.ForeignKey('user.id'))
    competition_id = Column(Integer, db.ForeignKey('competition.id'))
    score          = Column(Integer, default=0)
    
    
    def __init__(self, user_id: int, competition_id: int, score: int = 0):
        self.user_id = user_id
        self.competition_id = competition_id
        self.score = score


    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'competition_id': self.competition_id,
            'score': self.score
        }
        
    
    def __str__(self):
        return f"<Participant {self.id}: {self.user_id}, {self.competition_id}, {self.score}>"
    
    
    def __repr__(self):
        return self.__str__()