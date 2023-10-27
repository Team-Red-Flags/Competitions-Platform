from App.database import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Participant(db.Model):
    __tablename__  = "participant"
    user           = relationship('User', back_populates='participant')
    competition    = relationship('Competition', back_populates='participant')
    id             = Column(Integer, primary_key=True)
    user_id        = Column(Integer, ForeignKey('user.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competition.id'), nullable=False)
    score          = Column(Integer, default=0, nullable=True, unique=False)
    
    
    def __init__(self, user_id: int, competition_id: int, score: int = 0):
        self.user_id = user_id
        self.competition_id = competition_id
        self.score = score


    def get_json(self):
        return {
            'id' : self.id,
            'user_id': self.user_id,
            'competition_id': self.competition_id,
            'score': self.score
        }
        
    
    def __str__(self):
        return f"<Participant {self.id}: {self.user_id}, {self.competition_id}, {self.score}>"
    
    
    def __repr__(self):
        return self.__str__()