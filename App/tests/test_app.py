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
    update_user
)


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

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


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
        

