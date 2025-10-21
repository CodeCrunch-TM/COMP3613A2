from models import Student, Leaderboard
from App.database import db
from datetime import datetime

def create_student(name, email, password, programme):
    student = Student(name=name, email=email, password=password, programme=programme)
    db.session.add(student)
    db.session.commit()
    return {"message": f'Student "{name}" created!'}
    
def add_student_record(student_id, hours):
    student = Student.query.get(student_id)
    if not student:
        return {"error": f"No student found with ID {student_id}."}
    student.createRecord(hours, datetime.now().date()) #using current date for simplicity
    return {"message": f"Record of {hours} hours added for student ID {student_id}."}
    
def view_leaderboard(num_students):
    leaderboard = Leaderboard.getPodium(num_students)
    if not leaderboard:
        return {"error": "No entries in the leaderboard."}
    return [student.to_json() for student in leaderboard]
        #print(f"Position: {student['position']}, StudentID: {student['studentID']}, TotalHours: {student['totalHours']}")
        
def view_my_position(student_id):
    leaderboard = Leaderboard()
    position = leaderboard.findStudentPosition(student_id)
    if not position:
        return {"error": "No leaderboard entry found."}
    return {"message": f"Your Position: {position['position'] + 1}, Total Hours: {position['totalHours']}"}
    
def get_my_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found."}
    accolades = student.getAccolades()
    if not accolades:
        return {"error": "No accolades found."}
    else:
        return [accolade for accolade in accolades]
