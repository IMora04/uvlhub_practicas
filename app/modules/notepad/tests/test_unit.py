import pytest
from app.modules.notepad.services import NotepadService
from app.modules.notepad.models import Notepad
from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile

notepad_service = NotepadService()

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client

def test_get_all_notepads_returns_list(test_client):
    userId = 1
    result = notepad_service.get_all_by_user(userId)
    assert isinstance(result, list)
    assert all(isinstance(t, Notepad) for t in result)

def test_create_notepad(test_client):
    userId = 1
    initialLen = len(notepad_service.get_all_by_user(userId))
    createdNotepad = notepad_service.create(title="test", body="test", user_id=userId)
    newNotepads = notepad_service.get_all_by_user(userId)
    assert len(newNotepads) == initialLen + 1
    assert createdNotepad in newNotepads
    assert createdNotepad.title == "test"
