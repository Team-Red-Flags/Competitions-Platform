import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Admin, Competition, Participant
from App.controllers import (
    get_all_students_json,
    authenticate_admin,
    authenticate_student,
    get_admin,
    get_student,
    update_user,
    create_competition,
    get_competition,
    get_all_competitions
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

# Base user unit tests
class UserUnitTests(unittest.TestCase):
    
    test_username = 'bob'
    test_password = 'bobpass'
    
    def test_new_user(self):
        user = User(username=self.test_username, password=self.test_password)
        assert user.username == self.test_username
        
    def test_get_json(self):
        user = User(username=self.test_username, password=self.test_password)
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":self.test_username})

    def test_is_admin(self):
        user = User(username=self.test_username, password=self.test_password)
        assert user.is_admin() != True

    def test_check_password(self):
        user = User(username=self.test_username, password=self.test_password)
        assert user.check_password(self.test_password)
    
    def test_hashed_password(self):
        hashed = generate_password_hash(self.test_password, method='sha256')
        user = User(username=self.test_username, password=self.test_password)
        assert user.password != self.test_password


# Student user unit tests
class StudentUnitTests(unittest.TestCase):
    
    test_username = 'rob'
    test_password = 'robpass'
    test_fname = 'Rob'
    test_lname = 'Robinson'
    test_student_id = 80012346
    test_student_email = 'rob.robinson@my.uwi.edu'
    test_dob = date(1998, 1, 4)

    def test_new_student(self):
        student = Student(
            username=self.test_username,
            password=self.test_password,
            fname=self.test_fname,
            lname=self.test_lname,
            student_id=self.test_student_id,
            student_email=self.test_student_email,
            dob = self.test_dob
        )
        assert student.username == self.test_username
    
    def test_get_json(self):
        student = Student(
            username=self.test_username,
            password=self.test_password,
            fname=self.test_fname,
            lname=self.test_lname,
            student_id=self.test_student_id,
            student_email=self.test_student_email,
            dob = self.test_dob
        )
        student_json = student.get_json()
        self.assertDictEqual(student_json, {
            "id": None,
            "username": self.test_username,
            "student_id": self.test_student_id,
            "fname" : self.test_fname,
            "lname" : self.test_lname,
            "student_email" : self.test_student_email,
            "dob" : self.test_dob
        })

    def test_is_admin(self):
        student = Student(
            username=self.test_username,
            password=self.test_password,
            fname=self.test_fname,
            lname=self.test_lname,
            student_id=self.test_student_id,
            student_email=self.test_student_email,
            dob = self.test_dob
        )
        assert student.is_admin() != True

    def test_check_password(self):
        student = Student(
            username=self.test_username,
            password=self.test_password,
            fname=self.test_fname,
            lname=self.test_fname,
            student_id=self.test_student_id,
            student_email=self.test_student_email,
            dob = self.test_dob
        )
        assert student.check_password(self.test_password)
    
    def test_hashed_password(self):
        hashed = generate_password_hash(self.test_password, method='sha256')
        student = Student(
            username=self.test_username,
            password=self.test_password,
            fname=self.test_fname,
            lname=self.test_fname,
            student_id=self.test_student_id,
            student_email=self.test_student_email,
            dob = self.test_dob
        )
        assert student.password != self.test_password
    
# Admin user unit tests
class AdminUnitTests(unittest.TestCase):
    
    def test_new_admin(self):
        admin= Admin(
            username = 'ade',
            password = 'adepass',
            fname = 'ade',
            lname = 'b' 
        )
        assert admin.username == 'ade'

    def test_get_json(self):
        admin = Admin(
            username = 'ade',
            password = 'adepass',
            fname = 'ade',
            lname = 'b'   
        )
        admin_json= admin.get_json()
        self.assertDictEqual(admin_json, {"id":None, "username":"ade"})

    def test_is_admin(self):
        admin= Admin(
            username = 'ade',
            password = 'adepass',
            fname = 'ade',
            lname = 'b',
        )
        assert admin.is_admin() != True
    
    def test_check_password(self): 
        password = "adepass"
        admin= Admin(
            username = 'ade',
            password = 'adepass',
            fname = 'ade',
            lname = 'b'
        )
        assert admin.check_password(password)
    
    def test_hashed_password(self): 
        password = "adepass"
        hashed = generate_password_hash(password, method='sha256')
        student = Student(
            username = 'ade',
            password = password,
            fname = 'ade',
            lname = 'b',
        )
        assert student.password == hashed
    



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
    assert authenticate_user("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "rickpass")
        assert user.username == "rick"
    
    def test_create_competition(self):
        competition = create_competition("test", "test", "1 January, 2020", "10 January, 2020")
        assert competition.name == "test"
        
    def test_get_all_students_json(self):
        students_json = get_all_students_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_get_competition(self):
        competition = get_competition(1)
        assert competition.id == 1

    def test_get_all_competitions(self):
        competitions = get_all_competitions()
        for competition in competitions:
            assert competition.name == "test"
