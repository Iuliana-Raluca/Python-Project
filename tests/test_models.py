import pytest
from app.models import User, OperationLog
from werkzeug.security import check_password_hash
from datetime import datetime

def test_user_creation():
    user = User(username="testuser", role="admin")
    user.set_password("secret123")

    assert user.username == "testuser"
    assert user.role == "admin"
    assert user.password_hash != "secret123"  # parola trebuie hash-uita
    assert check_password_hash(user.password_hash, "secret123")
    assert user.check_password("secret123") is True
    assert user.check_password("wrong") is False


def test_operation_log_creation():
    log = OperationLog(
        operation="fibbo",
        input_data="n=10",
        result="55",
        status_code=200,
        timestamp=datetime.utcnow()
    )

    assert log.operation == "fibbo"
    assert log.input_data == "n=10"
    assert log.result == "55"
    assert log.status_code == 200
    assert isinstance(log.timestamp, datetime)
