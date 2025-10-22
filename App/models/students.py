from App.database import db
from .studentrecord import StudentRecord
from .user import User

class Student(User):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    programme = db.Column(db.String(100), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    } #inheritance
    
    def __init__(self, name, email, password, programme):
        super().__init__(name, email, password)
        self.programme = programme
    
    def __repr__(self):
        return f"<Student ID: {self.id}, Name: {self.name}, Email: {self.email}, Programme: {self.programme}>"

    def createRecord(self, hours, date):
        record = StudentRecord(studentID=self.id, hours=hours, datePerformed=date, status='Pending')
        db.session.add(record)
        db.session.commit()
        return record
    
    def getLeaderboardPosition(self):
        pos = self.leaderboard_entry
        return pos.position if pos else None
    # gotta test this, not sure if works
    
    def getTotalHours(self):
        pos = self.leaderboard_entry
        return pos.totalHours if pos else 0.0
    # also test this
    
    def getAccolades(self):
        return [{
                "accoladeID": accolade.accoladeID,
                "studentID": accolade.studentID,
                "accoladeTier": accolade.accoladeTier,
                "awardedBy": accolade.awardedBy
                } for accolade in self.accolades]
    # trying conversion here since it was breaking in controller, also manually structuring dict
    # fixed it, was sending the direct SQLAlchemy objects back which can't be serialized directly, so instead we send over a list of dicts that represent the accolades, and can just filter directly if needed instead of
    # at the function itself