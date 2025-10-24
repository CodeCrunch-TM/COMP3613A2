from App.database import db
from .accolades import Accolades
from .user import User
from .studentrecord import StudentRecord

class Staff(User):
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    } #inheritance
    
    def __init__(self, name, email, password, department):
        super().__init__(name, email, password)
        self.department = department
    
    def __repr__(self):
        return f"<Staff ID: {self.id}, Name: {self.name}, Email: {self.email}, Department: {self.department}>"

    # def getPendingRecords(self):
    #     return [record for record in self.student_records if record.status == 'Pending']
    #autocompleted logic, unsure if works
    
    def confirmRecord(self, recordID):
        record = StudentRecord.query.filter_by(recordID=recordID).first()
        # if record is None:
        #     print(f"No record found with ID {record.recordID}.")
        #     return False
        if record.isPending():
            record.setStatus('Confirmed')
            record.signRecord(self.id)
            db.session.commit()
            #placeholder for if wsgi command to update hours doesn't work, will just add here to autorun it
            #Leaderboard().updateHours(record.studentID, record.hours) or some variation on this, don't forget to import if doing this
            # print(f"Record {record.recordID} confirmed") # debug
            return True
        return False
        # i used this as a bool? i can't even remember what i was thinking
        
    def rejectRecord(self, recordID):
        record = StudentRecord.query.filter_by(recordID=recordID).first()
        # if record is None: # this check is redundant since controller already checks for record existence
        #     print(f"No record found with ID {record.recordID}.")
        #     return False
        if record and record.isPending(): # additional safety net, already checked in controller but i'll leave the logic here
            record.setStatus('Rejected')
            # print(f"Record {record.recordID} rejected") # debug
            record.signRecord(self.id)
            db.session.commit()
            return True
        return False
    # i'll leave them as bool incase i wanna check true/false on it later for whatever reason, won't change anything now cause it works and isn't necessarily wrong

    def giveAward(self, studentID, accoladeTier):
        if Accolades().isDupe(studentID, accoladeTier):
            return {"error": f"Duplicate accolade for student {studentID} at tier {accoladeTier}"} # passing forward
        elif not Accolades().isEligible(studentID, accoladeTier):
            return {"error" : f"Student {studentID} not eligible for accolade tier {accoladeTier}"} # same here
        accolade = Accolades(studentID=studentID, accoladeTier=accoladeTier, awardedBy=self.id)
        db.session.add(accolade)
        db.session.commit()
        return accolade
        # didn't do true false for this one, really couldn't tell you why i forgot what i was thinking at that time