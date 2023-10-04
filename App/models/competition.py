from App.database import db

class Competition(db.Model):
    __tablename__="competition"
    id = db.Column(db.Integer, primary_key=True)

