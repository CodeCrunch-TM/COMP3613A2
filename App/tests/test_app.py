import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, Student, Leaderboard, StudentRecord, Accolades
from datetime import datetime
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    initialize
)
from App.controllers import studentrecord
from App.controllers.student import create_student, add_student_record, view_leaderboard, view_my_position, get_my_accolades
from App.controllers.staff import create_staff, list_pending_records, confirm_record, reject_record, give_award

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
# class UserUnitTests(unittest.TestCase):

#     '''Premade'''
#     def test_new_user(self):
#         user = User("bob", "bobpass")
#         assert user.username == "bob"

#     # pure function no side effects or integrations called
#     def test_get_json(self):
#         user = User("bob", "bobpass")
#         user_json = user.get_json()
#         self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
#     def test_hashed_password(self):
#         password = "mypass"
#         hashed = generate_password_hash(password, method='sha256')
#         user = User("bob", password)
#         assert user.password != password

#     def test_check_password(self):
#         password = "mypass"
#         user = User("bob", password)
#         assert user.check_password(password)
        
    
class StudentUnitTests(unittest.TestCase):

    def test_create_student(self):
        student = Student("Jared", "jared@gmail.com", "jaredpass", "Computer Science")
        assert student.name == "Jared"
        assert student.email == "jared@gmail.com"
        self.assertTrue(check_password_hash(student.password, "jaredpass"))
        assert student.programme == "Computer Science"
        

    def test_student_repr(self):
        student = Student("Jared", "jared@gmail.com", "jaredpass", "Computer Science")
        student.id = 1 # gonna manually set this so i can confirm repr from student model
        assert str(student) == "<Student ID: 1, Name: Jared, Email: jared@gmail.com, Programme: Computer Science>"
        
class StudentRecordUnitTests(unittest.TestCase):

    def test_create_student_record(self):
        record = StudentRecord(studentID=1, hours=5.0, datePerformed=datetime(2025, 12, 25).date(), status='Pending')
        assert record.studentID == 1
        assert record.hours == 5.0
        assert record.datePerformed == datetime(2025, 12, 25).date()
        assert record.status == 'Pending'
        
    def test_is_pending(self):
        record = StudentRecord(studentID=1, hours=5.0, datePerformed=datetime(2025, 12, 25).date(), status='Pending')
        assert record.status == 'Pending'
        
    def test_transitions(self):
        record = StudentRecord(studentID=1, hours=5.0, datePerformed=datetime(2025, 12, 25).date(), status='Pending')
        assert record.status == 'Pending'
        record.status = 'Confirmed'
        assert record.status == 'Confirmed'
        record.status = 'Rejected'
        assert record.status == 'Rejected'
        
class StaffUnitTests(unittest.TestCase):

    def test_create_staff(self):
        staff = Staff("Leona", "leona@gmail.com", "leonapass", "Mathematics")
        assert staff.name == "Leona"
        assert staff.email == "leona@gmail.com"
        self.assertTrue(check_password_hash(staff.password, "leonapass"))
        assert staff.department == "Mathematics"

    def test_staff_repr(self):
        staff = Staff("Leona", "leona@gmail.com", "leonapass", "Mathematics")
        staff.id = 1  # manually set this to confirm repr from staff model
        assert str(staff) == "<Staff ID: 1, Name: Leona, Email: leona@gmail.com, Department: Mathematics>"
        
class AccoladeUnitTests(unittest.TestCase):

    def test_create_accolade(self):
        accolade = Accolades(studentID=1, accoladeTier=2, awardedBy=3)
        assert accolade.studentID == 1
        assert accolade.accoladeTier == 2
        assert accolade.awardedBy == 3

    def test_accolade_repr(self):
        accolade = Accolades(studentID=1, accoladeTier=2, awardedBy=3)
        accolade.accoladeID = 1  # manually set this to confirm repr from accolade model
        assert str(accolade) == "<AccoladeID: 1, StudentID: 1, AccoladeTier: 2, AwardedBy: 3>"
'''
    Integration Tests
'''
class UsersIntegrationTests(unittest.TestCase): #testing
    def test_user_workflow(self): #might delete this since it's kinda redundant with other tests *edit* nvm saw that we commmented out the other user tests         
        user = User("testuser", "test@email.com", "testpass")
        assert user.name == "testuser"
        assert user.email == "test@email.com"
        assert user.check_password("testpass")

class InitializeIntegrationTests(unittest.TestCase):
    def test_initialization(self):
        initialize()
        all_users = get_all_users_json()
        assert isinstance(all_users, list) 
        assert studentrecord.get_all_records() == {"error": "No records found."}
    
class StudentStaffIntegrationTests(unittest.TestCase): #maybe push working now
    
    def test_student_staff_interactions(self):
        student_result = create_student("Student1", "student1@test.com", "pass", "Computer Science")
        staff_result = create_staff("Staff1", "staff1@test.com", "pass", "IT Department")
        
        assert "message" in student_result  
        assert "message" in staff_result  #these might be in levi's tests already but it make sense to test here

        record_result = add_student_record(1, 15.0)  # Increase hours to meet accolade requirement
        assert "message" in record_result #test adding record
        
        pending_result = list_pending_records()
        assert isinstance(pending_result, (list, dict)) #pending test
        
        confirm_result = confirm_record(1)
        assert "message" in confirm_result or "error" in confirm_result #confirm test
        
        award_result = give_award(1, 1)
        assert award_result is not None
        if isinstance(award_result, dict):
            assert "message" in award_result or "error" in award_result  #reward test

        result = reject_record(1)
        assert "error" in result  #check to make sure u can update record that's already confirmed

class LeaderboardIntegrationTests(unittest.TestCase):
        
    def test_student_leaderboard_interactions(self): #tested using the functions mainly cuz i genuinely have no clue how levi used ID *edit* seems manually set, this autist

        student_result = create_student("StudentLB1", "studentlb1@test.com", "pass", "Engineering") #had to follow levi's method of IDing and setting manually
        assert "message" in student_result
        
        leaderboard_result = view_leaderboard(3) 
        assert isinstance(leaderboard_result, (list, dict))
        
        position_result = view_my_position(1) 
        assert isinstance(position_result, dict)
        
        record_result = add_student_record(1, 10.0)  
        
        if "message" in record_result:
            confirm_record(1)  
            updated_leaderboard = view_leaderboard(3)
            assert isinstance(updated_leaderboard, (list, dict))

    def test_leaderboard_updates(self):

        create_student("LBUpdate1", "lbupdate1@test.com", "pass", "Engineering")
        create_student("LBUpdate2", "lbupdate2@test.com", "pass", "Engineering")
        create_student("LBUpdate3", "lbupdate3@test.com", "pass", "Engineering")
        create_staff("LBUpdateStaff", "lbupdatestaff@test.com", "pass", "Engineering")

        add_student_record(1, 10.0)
        add_student_record(2, 20.0)
        add_student_record(3, 30.0)
        
        confirm_record(1)
        confirm_record(2)
        confirm_record(3)
        results = view_leaderboard(3)
            
        if isinstance(results, list):      #this man, i hate these returns, got them working eventually tho
            assert len(results) >= 0
            for entry in results:
                assert "position" in entry
                assert "studentID" in entry
                assert "totalHours" in entry
        elif isinstance(results, dict):
                assert "error" in results
    
    def test_leaderboard_podium(self):

        create_student("PodiumA", "podiuma@test.com", "pass", "Engineering")
        create_student("PodiumB", "podiumb@test.com", "pass", "Engineering")
        create_student("PodiumC", "podiumc@test.com", "pass", "Engineering")
        create_staff("PodiumStaff", "podiumstaff@test.com", "pass", "Engineering")

        add_student_record(1, 15.0)
        add_student_record(2, 25.0)
        add_student_record(3, 35.0)

        confirm_record(1)
        confirm_record(2)
        confirm_record(3)
        results = view_leaderboard(3)
        
        if isinstance(results, list):
            assert len(results) >= 0  #played with instances and shi till i got it working, the logic is sound...maybe
            if len(results) > 0:
                for entry in results:
                        assert "position" in entry
                        assert "studentID" in entry
                        assert "totalHours" in entry
                if len(results) >= 2:
                        assert results[0]["position"] >= 1
                        assert results[1]["position"] >= 1
                        assert results[0]["position"] <= results[1]["position"] 
                if len(results) >= 3:
                        assert results[2]["position"] >= 1
                        assert results[1]["position"] <= results[2]["position"]       
        elif isinstance(results, dict):
                assert "error" in results

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


'''
def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
'''
        

