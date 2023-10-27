from App.database import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

class Competition(db.Model):
    __tablename__ = "competition"
    participant = relationship('Participant', cascade='all, delete-orphan')
    id          = Column(Integer, primary_key=True)
    name        = Column(String(80), nullable=False, unique=True)
    description = Column(String(200), nullable=False)
    start_date  = Column(Date, nullable=True)
    end_date    = Column(Date, nullable=True)


    def __init__(self, name, description, start_date, end_date = None):
        self.name        = name
        self.description = description if description else "A new competition!"
        self.start_date  = start_date
        self.end_date    = end_date
        
        
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description' : self.description,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        
    
    def __str__(self):
        return f"<Competition {self.id}: {self.name}>"


    def __repr__(self):
        return self.__str__()