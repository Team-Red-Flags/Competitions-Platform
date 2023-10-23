from App.database import db
from App.models import User, Competition
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Participant(db.Model):
    __tablename__ = "participant"
    id               = Column(Integer, primary_key=True)
    user             = relationship('User')
    competition      = relationship('Competition')
    user_id          = Column(Integer, ForeignKey('user.id'))
    competition_id   = Column(Integer, ForeignKey('competition.id'))
    score            = Column(Integer, default=0)
    
    
    def __init__(self, user_id: int, competition_id: int, score: int = 0):
        self.user_id = user_id
        self.competition_id = competition_id
        self.score = score


    def get_json(self):
        return {
            'user_id': self.user_id,
            # 'username':  User.query.get(self.user_id).username,
            'competition_id': self.competition_id,
            # 'competition_name': Competition.query.get(self.competition_id).name,
            'score': self.score
        }
        
    
    def __str__(self):
        return f"<Participant {self.id}: {self.user_id}, {self.competition_id}, {self.score}>"
    
    
    def __repr__(self):
        return self.__str__()