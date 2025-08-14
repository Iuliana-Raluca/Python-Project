import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_create_user(app_context):
    user = User(username="testuser", role="user")
    user.set_password("secret123")

    assert user.username == "testuser"
    assert user.role == "user"
    assert user.password_hash is not None
    assert isinstance(user.password_hash, str)

def test_password_hashing(app_context):
    user = User(username="secureuser", role="admin")
    user.set_password("mypassword")

    assert user.check_password("mypassword") is True
    assert user.check_password("wrongpass") is False

