from App.database import db

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    
    studentID = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True, nullable=False)
    totalHours = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    
    student = db.relationship('Student', backref=db.backref('leaderboard', lazy=True))
    
    def __repr__(self):
        return f"<Leaderboard StudentID: {self.studentID}, TotalHours: {self.totalHours}, Position: {self.position}>"
    
    @staticmethod
    def recalculatePositions():
        # print("Recalculating leaderboard positions...") # pretty much exclusively debug, just to see that it triggers.
        entries = Leaderboard.query.order_by(Leaderboard.totalHours.desc()).all() #grabs all entries
        for pos, entry in enumerate(entries, start=1): #for loop location swap - enumerate gives index and value
            entry.position = pos
        db.session.commit()
        return entries # i think this works? i tested and i still think it works?
    
    
    @staticmethod
    def getPodium(numStudents):
        podium = []
        for position in range(0, numStudents+1):
            entry = Leaderboard.query.filter_by(position=position).first()
            if entry:
                podium.append({
                    'position': entry.position,
                    'studentID': entry.studentID,
                    'totalHours': entry.totalHours
                })
                # just stacking dicts in a list, should be easy to parse
        return podium


    def findStudentPosition(self, studentID):
        entry = Leaderboard.query.filter_by(studentID=studentID).first()
        if entry:
            return {
                'position': entry.position,
                'studentID': entry.studentID,
                'totalHours': entry.totalHours
            }
        return None
        #test this too - works
        
    def updateHours(self, studentID, additionalHours):
        entry = Leaderboard.query.filter_by(studentID=studentID).first()
        if entry:
            entry.totalHours += additionalHours
            Leaderboard.recalculatePositions()
            # print(f"Updated hours for student {studentID} to {entry.totalHours}") # debugging stuff
            db.session.commit()
            return {"update" : f"Updated hours for student {studentID} to {entry.totalHours}"}
        elif not entry: #I FORGOT TO ADD IF IT DIDN'T EXIST I JUST SPENT AN HOUR DEBUGGING AND COULDN'T FIND ITTTTTTTTT
            new_entry = Leaderboard(studentID=studentID, totalHours=additionalHours, position=0) #position is placeholder
            db.session.add(new_entry)
            db.session.commit()
            Leaderboard.recalculatePositions() # position doesn't matter cause will recalc anyways
            # print(f"Created new leaderboard entry for student {studentID} with {additionalHours} hours")
            return {"update" : f"Created new leaderboard entry for student {studentID} with {additionalHours} hours"} # added update messages incase i wanna use them later
        #every time staff confirms a record, it should call this
        
    