import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
#yes i did ai this, it was bothering me - package deprecation warnings

from App.database import db, get_migrate
from App.models import User, Staff, Student, StudentRecord, Accolades, Leaderboard
import App.controllers.staff as staffController
import App.controllers.student as studentController
import App.controllers.studentrecord as studentrecordController
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
def create_staff_command(name, email, password, department): #
    execution = staffController.create_staff(name, email, password, department)
    print(execution.get("message"))

#list pending records for staff to confirm/reject
@staff.command("list_pending", help="List all pending student records")
def list_pending_records_command():
    execution = staffController.list_pending_records()
    if "error" in execution:
        print(execution.get("error"))
        return
    for record in execution:
        print(record)

#list all records, mainly for testing purposes but maybe useful as log
@staff.command("list_all", help="List all student records")
def list_all_records(): #
    records = studentrecordController.get_all_records()
    if "error" in records:
        print(records.get("error"))
        return
    for record in records: #dumb but should work
        print(record)

#staff confirmation, should also update leaderboard hours and standings
@staff.command("confirm_record", help="Confirm a student record by ID")
@click.argument("record_id", type=int)
def confirm_record_command(record_id): #
    execution = staffController.confirm_record(record_id)
    if "error" in execution:
        print(execution.get("error"))
        return
    print(execution.get("message"))

#i don't think i really need to explain this one
@staff.command("reject_record", help="Reject a student record by ID")
@click.argument("record_id", type=int)
def reject_record_command(record_id): #
    execution = staffController.reject_record(record_id)
    if "error" in execution:
        print(execution.get("error"))
        return
    print(execution.get("message"))

#allows a staff member to give an accolade to a student if eligible and not a dupe
@staff.command("give_award", help="Give an accolade to a student")
@click.argument("student_id", type=int)
@click.argument("accolade_tier", type=int)
def give_award_command(student_id, accolade_tier): #
    execution = staffController.give_award(student_id, accolade_tier)
    if "error" in execution:
        print(execution.get("error"))
        return
    print(execution.get("message"))
   
    
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
def create_student_command(name, email, password, programme): #
    execution = studentController.create_student(name, email, password, programme)
    # didn't add an error for this, if one is added then it'll go here ~Levi
    print(execution.get("message"))
    
#student command to add a record
@student.command("add_record", help="Add a student record")
@click.argument("student_id", type=int)
@click.argument("hours", type=float)
def add_student_record_command(student_id, hours): #
    execution = studentController.add_student_record(student_id, hours)
    if "error" in execution:
        print(execution.get("error"))
        return
    print(execution.get("message"))
 
 
#student command to view leaderboard, also how students get their total hours viewed, might add a filtered version for only one student later   
@student.command("leaderboard", help="View the leaderboard")
@click.argument("num_students", type=int, default=3)
def view_leaderboard_command(num_students): #
    leaderboard = studentController.view_leaderboard(num_students)
    if "error" in leaderboard:
        print(leaderboard.get("error"))
        return
    print(f"Top {num_students} Students in the Leaderboard:")
    for entry in leaderboard:
        print(f"Position: {entry['position']}, StudentID: {entry['studentID']}, TotalHours: {entry['totalHours']}")
    
    
#student command to find their position, because there's no current user logic, this will require manual user input of student ID 
@student.command("my_position", help="View your leaderboard position")
@click.argument("student_id", type=int)
def view_my_position_command(student_id): #
    execution = studentController.view_my_position(student_id)
    if "error" in execution:
        print(execution.get("error"))
        return
    print(execution.get("message"))
    
        
#allows a student to view their accolades, same logic as above     
@student.command("my_accolades", help="View your accolades")
@click.argument("student_id", type=int)
def get_my_accolades_command(student_id): #
    accolades = studentController.get_my_accolades(student_id)
    if "error" in accolades:
        print(accolades.get("error"))
        return
    else:
        print(f"Accolades for Student ID {student_id}:")
        for accolade in accolades:
            print(f"Accolade ID: {accolade['accoladeID']}, Tier: {accolade['accoladeTier']}, Awarded By: {accolade['awardedBy']}")
        
        
app.cli.add_command(student)
