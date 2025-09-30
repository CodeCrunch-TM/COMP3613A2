from App.database import db
from .leaderboard import Leaderboard

class Accolades(db.Model):
    __tablename__ = 'accolades'
    
    accoladeID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    accoladeTier = db.Column(db.Integer, nullable=False)
    awardedBy = db.Column(db.String(100), db.ForeignKey('staff.id'), nullable=False)
    
    student = db.relationship('Student', backref=db.backref('accolades', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('accolades', lazy=True))

    def __repr__(self):
        return f"<Accolades ID: {self.accoladeID}, StudentID: {self.studentID}, AccoladeTier: {self.accoladeTier}, AwardedBy: {self.awardedBy}>"
    
    def isDupe(self, studentID, accoladeTier):
        existing = Accolades.query.filter_by(studentID=studentID, accoladeTier=accoladeTier).first()
        return existing is not None
        
        
    def isEligible(self, studentID, accoladeTier):
        entry = Leaderboard.query.filter_by(studentID=studentID).first()
        if not entry:
            return False
        
        tier_requirements = {1: 10, 2: 25, 3: 50}
        required_hours = tier_requirements.get(accoladeTier, float('inf')) #python has positive infinity as 'inf'
        
        return entry.totalHours >= required_hours #inf is failsafe for anything not declared in dict, should be brute force safe -- havent' tested fully
    
    # def getAccolades(self, studentID):
    #     return Accolades.query.filter_by(studentID=studentID).all()