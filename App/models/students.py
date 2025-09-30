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
        print(f"Record {record.recordID} created for {self.name}")
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
        return self.accolades
    # test for formatting, etc