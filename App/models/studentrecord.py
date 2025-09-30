from App.database import db

class StudentRecord(db.Model):
    __tablename__ = 'student_records'
    
    recordID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    datePerformed = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    student = db.relationship('Student', backref=db.backref('student_records', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('student_records', lazy=True))

    def __repr__(self):
        return f"<StudentRecord ID: {self.recordID}, StudentID: {self.studentID}, StaffID: {self.staffID}, Date: {self.datePerformed}, Hours: {self.hours}, Status: {self.status}>"
    
    def isPending(self):
        return self.status == 'Pending'
    
    def setStatus(self, newStatus):
        self.status = newStatus
        db.session.commit()
        return self.status
    
    def signRecord(self, staffID):
        self.staffID = staffID
        db.session.commit()
        return self.staffID
    
    @staticmethod
    def getRecords():
        return StudentRecord.query.all()
        
    @staticmethod
    def getPendingRecords():
        return StudentRecord.query.filter_by(status='Pending').all()
        