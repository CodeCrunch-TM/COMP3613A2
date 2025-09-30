import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
#yes i did ai this, it was bothering me - package deprecation warnings

from App.database import db, get_migrate
from App.models import User, Staff, Student, StudentRecord, Accolades, Leaderboard
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    #initializing users for testing
    staff1 = Staff(name="Sally", email="sally@example.com", password="sallypass", department="HR")
    student1 = Student(name="Bob", email="bob@example.com", password="bobpass", programme="Computer Science")
    db.session.add_all([staff1, student1])
    db.session.commit()
    print('database initialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
Staff Commands
'''

staff = AppGroup('staff', help='Staff object commands')

#staff command to create a staff member
@staff.command("create", help="Creates a staff member")
@click.argument("name")
@click.argument("email")
@click.argument("password")
@click.argument("department")
def create_staff_command(name, email, password, department):
    staff = Staff(name=name, email=email, password=password, department=department)
    db.session.add(staff)
    db.session.commit()
    print(f'Staff member {name} created!')


#list pending records for staff to confirm/reject
@staff.command("list_pending", help="List all pending student records")
def list_pending_records():
    records = StudentRecord.getPendingRecords()
    if not records:
        print("No pending records found.")
    for record in records:
        print(record)

#list all records, mainly for testing purposes but maybe useful as log
@staff.command("list_all", help="List all student records")
def list_all_records():
    records = StudentRecord.getRecords()
    for record in records:
        print(record)
    if not records:
        print("No records found.")
        
        
#staff confirmation, should also update leaderboard hours and standings
@staff.command("confirm_record", help="Confirm a student record by ID")
@click.argument("record_id", type=int)
def confirm_record(record_id):
    staff = Staff.query.first()  # not sure if to add current user logic since we're just doing cli
    if not staff:
        print("Ain't nobody home")
        return

    record = StudentRecord.query.get(record_id) # confirm that record exists, not misinput
    if not record:
        print(f"No record found with ID {record_id}.")
        return
    staff.confirmRecord(record_id)
    leaderboard = Leaderboard()
    if leaderboard.updateHours(record.studentID, record.hours):
        db.session.commit()
    
#i don't think i really need to explain this one
@staff.command("reject_record", help="Reject a student record by ID")
@click.argument("record_id", type=int)
def reject_record(record_id):
    staff = Staff.query.first() # once again, i do not know if i should allow this to just be free, but for testing purposes it should be fine
    if not staff:
        print("Ain't nobody home")
        return
    record = StudentRecord.query.get(record_id) # confirm that record exists, not misinput
    if not record:
        print(f"No record found with ID {record_id}.")
        return
    staff.rejectRecord(record_id)

#allows a staff member to give an accolade to a student if eligible and not a dupe    
@staff.command("give_award", help="Give an accolade to a student")
@click.argument("student_id", type=int)
@click.argument("accolade_tier", type=int)
def give_award(student_id, accolade_tier):
    staff = Staff.query.first() # i ain't saying it again
    if not staff:
        print("Ain't nobody home")
        return
    staff.giveAward(student_id, accolade_tier)
   
    
app.cli.add_command(staff)

'''
Student Commands
'''
student = AppGroup('student', help='Student object commands')

#student command to create a student
@student.command("create", help="Creates a student")
@click.argument("name")
@click.argument("email")
@click.argument("password")
@click.argument("programme")
def create_student_command(name, email, password, programme):
    student = Student(name=name, email=email, password=password, programme=programme)
    db.session.add(student)
    db.session.commit()
    print(f'Student {name} created!')

#student command to add a record
@student.command("add_record", help="Add a student record")
@click.argument("student_id", type=int)
@click.argument("hours", type=float)
def add_student_record(student_id, hours):
    student = Student.query.get(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        return
    student.createRecord(hours, datetime.now().date()) #using current date for simplicity
 
#student command to view leaderboard, also how students get their total hours viewed, might add a filtered version for only one student later   
@student.command("leaderboard", help="View the leaderboard")
@click.argument("num_students", type=int, default=3)
def view_leaderboard(num_students):
    leaderboard = Leaderboard.getPodium(num_students)
    if not leaderboard:
        print("No entries in the leaderboard.")
        return
    
    print(f"Top {num_students} Students in the Leaderboard:")
    for student in leaderboard:
        print(f"Position: {student['position']}, StudentID: {student['studentID']}, TotalHours: {student['totalHours']}")
        
#student command to find their position, because there's no current user logic, this will require manual user input of student ID 
@student.command("my_position", help="View your leaderboard position")
@click.argument("student_id", type=int)
def view_my_position(student_id):
    leaderboard = Leaderboard()
    position = leaderboard.findStudentPosition(student_id)
    if not position:
        print(f"No leaderboard entry found for student ID {student_id}.")
        return
    print(f"Your Position: {position['position'] + 1}, Total Hours: {position['totalHours']}")
        
#allows a student to view their accolades, same logic as above     
@student.command("my_accolades", help="View your accolades")
@click.argument("student_id", type=int)
def view_my_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        return
    accolades = student.getAccolades()
    for accolade in accolades:
        print(f"Accolade ID: {accolade.accoladeID}, Tier: {accolade.accoladeTier}, Awarded By: {accolade.awardedBy}")
        
app.cli.add_command(student)
