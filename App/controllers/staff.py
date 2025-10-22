from App.models import Staff, StudentRecord, Leaderboard
from App.database import db

def create_staff(name, email, password, department):
    staff = Staff(name=name, email=email, password=password, department=department)
    db.session.add(staff)
    db.session.commit()
    return {"message": f'Staff member "{name}" created!'}
    
def list_pending_records():
    records = StudentRecord.getPendingRecords()
    if not records:
        return {"error": "No pending records found."}
    else:
        return [dict(record) for record in records]
                        
def confirm_record(record_id):
    staff = Staff.query.first()  # not sure if to add current user logic since we're just doing cli
    if not staff:
        return {"error": "No staff member found."}

    record = StudentRecord.query.get(record_id) # confirm that record exists, not misinput
    if not record:
        return {"error": f"No record found with ID {record_id}."}
    if record.isPending() == False: # as below, so above
        return {"error": f"Record ID {record_id} is not pending and cannot be confirmed."}
    
    staff.confirmRecord(record_id)
    leaderboard = Leaderboard()
    # if leaderboard.updateHours(record.studentID, record.hours):
    #     db.session.commit()
    # looking at it, my updateHours function already commits, so this was basically just a double commit, didn't break anything but not needed.
    # IF CONFIRM BREAKS, READ ^^^
    leaderboard.updateHours(record.studentID, record.hours)
    return {"message": f"Record ID {record_id} has been confirmed."}
        
def reject_record(record_id):
    staff = Staff.query.first() # once again, i do not know if i should allow this to just be free, but for testing purposes it should be fine
    if not staff:
        return {"error": "No staff member found."}
    record = StudentRecord.query.get(record_id) # confirm that record exists, not misinput
    if not record:
        return {"error": f"No record found with ID {record_id}."}
    if record.isPending() == False: # changed from record.status != 'Pending' to the getter for pending instead, oop strikes again (Mainframe mainframe = new Mainframe(); @jon)
        return {"error": f"Record ID {record_id} is not pending and cannot be rejected."}
    staff.rejectRecord(record_id)
    return {"message": f"Record ID {record_id} has been rejected."}
    
def give_award(student_id, accolade_tier):
    staff = Staff.query.first() # i ain't saying it again
    if not staff:
        return {"error": "No staff member found."}
    award = staff.giveAward(student_id, accolade_tier)
    if "error" in award: #  receive any errors from model and pass it to wsgi
        return award
    return {"message": f"Accolade of tier {accolade_tier} given to student ID {student_id}."}