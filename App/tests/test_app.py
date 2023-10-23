import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Competition, Participant
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate_user,
    get_user,
    get_user_by_username,
    update_user,
    create_competition,
    get_competition,
    get_all_competitions

)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):
    # pure function no side effects or integrations called
    #User Unit Tests
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_is_admin(self):
        user = User("jane", "janepass", "admin")
        assert user.type == "admin"

    #competition unit tests
    def test_new_competition(self):
        competition = Competition("test", "test", "2020-01-01", "2020-01-01")
        assert competition.name == "test"

    def test_competition_description(self):
        competition = Competition("test", "2020-01-01", "2020-01-01")
        assert competition.description == "A new competition!"    

    def test_get_json_competition(self):
        competition = Competition("test", "test", "2020-01-01", "2020-01-01")
        competition_json = competition.get_json()
        self.assertDictEqual(competition_json, {"id":None, "name":"test", "description":"test", "start_date":"2020-01-01", "end_date":"2020-01-01"})

    #participant unit tests    
    def test_new_participant(self):
        participant = Participant (1, 1)
        assert participant.score == 0

    def test_get_json_participant(self):
        participant = Participant (1, 1)
        participant_json = participant.get_json()
        self.assertDictEqual(participant_json, {"id":None, "user_id":1, "competition_id":1, "score":0})
    
    #admin unit tests 
    def test_new_admin(self):
        user = User("jane", "janepass", "admin")
        assert user.type == "admin"



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

    def test_create_competition(self):
        competition = create_competition("test", "test", "2020-01-01", "2020-01-01")
        assert competition.name == "test"
    
    def test_get_competition(self):
        competition = get_competition()
        assert competition.name == "test"

    def test_get_all_competitions(self):
        competition = get_all_competitions()
        assert competition.name == "test"
