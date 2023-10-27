import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from App.main import create_app
from App.utils import get_date_from_string
from App.database import db, create_db
from App.models import User, Student, Admin, Competition
from App.controllers import (
    authenticate_user,
    get_user,
    create_user,
    update_user,
    get_all_users,
    get_all_users_json,
    get_user_by_username,
    get_student,
    create_student,
    update_student,
    get_all_students,
    get_all_students_json,
    get_student_by_username,
    get_admin,
    create_admin,
    update_admin,
    get_all_admins,
    get_all_admins_json,
    get_admin_by_username,
    get_competition,
    create_competition,
    update_competition,
    get_all_competitions,
    get_all_competitions_json,
    is_participant,
    get_participant,
    create_participant,
    get_top_20_participants,
    update_participant_score,
    get_competition_rankings,
    get_all_participants_json,
    get_participant_competitions
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
        self.assertDictEqual(user.get_json(), {"id":None, "username":self.test_username})

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
        self.assertDictEqual(student.get_json(), {
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


# Admin user unit tests
class AdminUnitTests(unittest.TestCase):
    
    test_username = 'ade'
    test_password = 'adepass'
    test_fname = 'Ade'
    test_lname = 'B'
    
    def test_new_admin(self):
        admin= Admin(
            username = self.test_username,
            password = self.test_password,
            fname = self.test_fname,
            lname = self.test_lname 
        )
        assert admin.username == self.test_username

    def test_get_json(self):
        admin = Admin(
            username = self.test_username,
            password = self.test_password,
            fname = self.test_fname,
            lname = self.test_lname
        )
        self.assertDictEqual(admin.get_json(), {
            "id": None, 
            "username": self.test_username, 
            "fname": self.test_fname, 
            "lname": self.test_lname
        })

    def test_is_admin(self):
        admin= Admin(
            username = self.test_username,
            password = self.test_password,
            fname = self.test_fname,
            lname = self.test_lname
        )
        assert admin.is_admin() == True


# Competition unit tests
class CompetitionUnitTests(unittest.TestCase):
    
    test_name = "Test Competition"
    test_start_date = "10-03-2024"
    test_end_date = "12-03-2024"
    
    def test_new_competition(self):
        competition = Competition(
            name=self.test_name,
            description="",
            start_date=self.test_start_date,
            end_date=self.test_end_date
        )
        assert competition.description == "A new competition!"
        
    def test_get_json(self):
        competition = Competition(
            name=self.test_name,
            description="",
            start_date=self.test_start_date,
            end_date=self.test_end_date
        )
        self.assertDictEqual(competition.get_json(), {
            "id": None,
            "name": self.test_name,
            "description": "A new competition!",
            "start_date": self.test_start_date,
            "end_date": self.test_end_date
        })



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
    
    def test_get_user(self):
        user = get_user(1)
        assert user.username == "bob"
    
    def test_get_user_json(self):
        user = get_user(1)
        self.assertDictEqual(user.get_json(), {
            "id": 1, 
            "username": "bob"
        })
    
    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual(users_json, [
            {"id":1, "username":"bob"}, 
            {"id":2, "username":"rick"}
        ])

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"



class StudentIntegrationTests(unittest.TestCase):
    
    def test_create_student(self):
        Student= create_student("rickpass", "rick100", "rick", "Doe", "2", "rick@my.uwi.edu", "02-02-2001")
        assert Student.username == "rickpass"


    def test_get_student(self):
        Student = get_student(1)
        if Student is None:
          return "Student not found"
        return Student
    

    def test_get_student_json(self):
        Student = get_student(1)
        expected_data = {
        "id": 1,
        "username": "bob"
    }
        if Student is None:
         return None
        self.assertDictEqual(Student.get_json, expected_data)
        

    def test_get_all_students_json(self):
        Student_json = get_all_students_json()
        expected_data = [
        {"id": 1, "username": "bob"},
        {"id": 2, "username": "rick"},
    ]
        self.assertListEqual(Student_json, expected_data)
   
        

    def test_get_student_by_username(self):
        Student = get_student_by_username("bob")
        if Student is None:
         return "Student with username not found"
        return Student
        
          

    def test_update_student(self):
        update_student(1, "ronnie")
        Student = get_student(1)
        if Student is None:
            return "Student not found"
        


class AdminIntegrationTests(unittest.TestCase):
    
    def test_create_admin(self):
        admin = create_admin("ade", "adepass", "Ade", "B")
        assert admin.username == "ade"
    
    def test_get_admin(self):
        admin = get_admin_by_username("ade")
        assert admin.username == "ade"
    
    def test_get_admin_json(self):
        admin = get_admin_by_username("ade")
        self.assertDictEqual(admin.get_json(),{
            "id": 3, 
            "username": "ade",
            'fname' : "Ade",
            'lname' : "B"
        })
    
    def test_get_all_admins_json(self):
        admins_json = get_all_admins_json()
        self.assertListEqual(admins_json, [
            {"id":1, "username":"ade"}, 
            {"id":2, "username":"kim"}
        ])
    
    def test_get_admin_by_username(self):
        admin = get_admin_by_username("ade")
        assert admin.username == "ade"
    
    def test_update_admin(self):
        update_admin(1, "ava")
        admin = get_admin_by_username("ava")
        assert admin.username == "ava"


class CompetitionIntegrationTests(unittest.TestCase):
    
    test_name = "Test Competition"
    test_start_date = "10-03-2024"
    test_end_date = "12-03-2024"

    competition = Competition(
            name=self.test_name,
            description="",
            start_date=self.test_start_date,
            end_date=self.test_end_date
        )
    assert competition.description == "A new competition!"
    
    def test_get_competition(self):
        competition = get_competition(1)
        assert competition.id == 1
    
    def test_get_competition_json(self):
        competition = Competition(
            name=self.test_name,
            description="",
            start_date=self.test_start_date,
            end_date=self.test_end_date
        )
        self.assertDictEqual(competition.get_json(), {
            "id": None,
            "name": self.test_name,
            "description": "A new competition!",
            "start_date": self.test_start_date,
            "end_date": self.test_end_date
        })
    
    def test_get_all_competitions_json(self):
        competition_json = get_competition(1)
        all_competitions_json = get_all_participants_json()
        assert type(all_competitions_json) == list
        assert type(all_competitions_json[0]) == dict
        self.assertDictContainsSubset(competition_json, dict(all_competitions_json[0]))

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_update_competition(self):
        update_competition(1, "New Competition")
        competition = get_competition(1)
        assert competition == "New Competition"

class ParticipantIntegrationTests(unittest.TestCase):
    
    test_user_id1 = 1
    test_user_id2 = None
    test_competition_id = 1
    
    def test_create_participant(self):
        participant = create_participant(
            user_id=self.test_user_id1,
            competition_id=self.test_competition_id
        )
        user = get_user(participant.user_id)
        assert user.username == "ronnie"
        
        # New student participant
        dave: Student = create_student(
            username="dave",
            password="davepass",
            fname="David",
            lname="George",
            student_id=80012349,
            student_email="david.george@my.uwi.edu",
            dob="1/5/2003"
        )
        new_participant = create_participant(dave.id, self.test_competition_id)
        assert new_participant.user_id == dave.id
        
            
    def test_get_participant(self):
        participant = get_participant(self.test_user_id1, self.test_competition_id)
        assert participant.id == self.test_user_id1
    
    def test_get_participant_competitions(self):
        competitions = get_participant_competitions(self.test_user_id1)
        competition = get_competition(self.test_competition_id)
        assert competitions != None
        assert type(competitions) == list
        assert type(competitions[0]) == Competition
        self.assertDictEqual(competitions[0].get_json(), competition.get_json())
    
    def test_get_all_participants_json(self):
        participant_json = get_participant(self.test_user_id1, self.test_competition_id).get_json()
        all_participants_json = get_all_participants_json()
        assert type(all_participants_json) == list
        assert type(all_participants_json[0]) == dict
        self.assertDictContainsSubset(participant_json, dict(all_participants_json[0]))
    
    def test_get_top_20_participants(self):
        update_participant_score(self.test_user_id1, self.test_competition_id, 40)
        update_participant_score(self.test_user_id2, self.test_competition_id, 90)
        participants = get_top_20_participants(self.test_competition_id)
        assert len(participants) == 2
        assert participants[0]['score'] > participants[1]['score']
        
    def test_update_participant_score(self):
        scores = [70, 65]
        self.test_user_id2 = get_user_by_username("dave").id
        
        update_participant_score(self.test_user_id1, self.test_competition_id, scores[0])
        participant = get_participant(self.test_user_id1, self.test_competition_id)
        assert participant.score == scores[0]

        update_participant_score(self.test_user_id2, self.test_competition_id, scores[1])
        participant = get_participant(self.test_user_id2, self.test_competition_id)
        assert participant.score == scores[1]
    