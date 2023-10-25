from App.database import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Participant(db.Model):
    __tablename__ = "participant"
    id               = Column(Integer, primary_key=True)
    user             = relationship('Student')
    competition      = relationship('Competition')
    student_id       = Column(Integer, ForeignKey('student.id'))
    competition_id   = Column(Integer, ForeignKey('competition.id'))
    score            = Column(Integer, default=0)
    
    
    def __init__(self, student_id: int, competition_id: int, score: int = 0):
        self.student_id = student_id
        self.competition_id = competition_id
        self.score = score


    def get_json(self):
        return {
            'student_id': self.student_id,
            'competition_id': self.competition_id,
            'score': self.score
        }
        
    
    def __str__(self):
        return f"<Participant {self.id}: {self.student_id}, {self.competition_id}, {self.score}>"
    
    
    def __repr__(self):
        return self.__str__()