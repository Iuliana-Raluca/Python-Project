import pytest, pytest_asyncio
from flask import Flask, request, session, jsonify
from app.validators import Validator, require_api_key, login_required, role_required

def test_validate_positive_int_valid():
    assert Validator.validate_positive_int("5") == 5
    assert Validator.validate_positive_int(10) == 10
    assert Validator.validate_positive_int(500, operation="factorial") == 500


def test_validate_positive_int_negative_value():
    with pytest.raises(ValueError, match="pozitiva"):
        Validator.validate_positive_int(-5)

def test_validate_positive_int_invalid_type():
    with pytest.raises(ValueError, match="intreg"):
        Validator.validate_positive_int(3.14)

def test_validate_positive_int_non_numeric_string():
    with pytest.raises(ValueError, match="intreg pozitiv"):
        Validator.validate_positive_int("abc")

def test_validate_positive_int_exceeds_max():
    with pytest.raises(ValueError, match="Limita este 500"):
        Validator.validate_positive_int(501, operation="factorial")


def test_safe_math_call_valid_result():
    def dummy_func(x): return x * 2
    assert Validator.safe_math_call(dummy_func, 5) == 10

def test_safe_math_call_none_result():
    def return_none(): return None
    with pytest.raises(ValueError, match="prea mare"):
        Validator.safe_math_call(return_none)

def test_safe_math_call_float_inf():
    def return_inf(): return float("inf")
    with pytest.raises(ValueError, match="prea mare"):
        Validator.safe_math_call(return_inf)

def test_safe_math_call_not_int():
    def return_float(): return 3.14
    with pytest.raises(ValueError, match="nu este un intreg valid"):
        Validator.safe_math_call(return_float)

def test_safe_math_call_exception():
    def raise_error(): raise OverflowError("Dummy error")
    with pytest.raises(ValueError, match="Eroare de calcul: Dummy error"):
        Validator.safe_math_call(raise_error)

#teste cu cheie corecta
@pytest.mark.asyncio
async def test_require_api_key_valid(monkeypatch):
    app = Flask(__name__)
    app.config["API_KEY"] = "123AB"

    @app.route("/test")
    @require_api_key
    async def protected(): return "OK"

    with app.test_request_context(headers={"X-API-KEY": "123AB"}):
        response = await protected()
        assert response == "OK"

#teste cu cheie invalida sau lipsa
@pytest.mark.asyncio
async def test_require_api_key_invalid(monkeypatch):
    app = Flask(__name__)
    app.config["API_KEY"] = "123"

    @app.route("/test")
    @require_api_key
    async def protected(): return "OK"

    with app.test_request_context(headers={"X-API-KEY": "wrong"}):
        response = await protected()
        assert response[1] == 401
        assert "lipsa" in response[0].json["error"]

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test"
    return app

def test_login_required_user_present(app):
    @login_required
    def protected():
        return "success"

    with app.test_request_context():
        session["user"] = {"username": "test"}
        assert protected() == "success"

def test_login_required_user_missing(app):
    @login_required
    def protected():
        return "success"

    with app.test_request_context():
        if "user" in session:
            session.pop("user")
        response = protected()
        assert response.status_code == 302
        assert "/login" in response.location

def test_role_required_success(app):
    @role_required("admin")
    def protected():
        return "ok"

    with app.test_request_context():
        session["user"] = {"role": "admin"}
        assert protected() == "ok"

def test_role_required_wrong_role(app):
    @role_required("admin")
    def protected():
        return "ok"

    with app.test_request_context():
        session["user"] = {"role": "user"}
        response, status = protected()
        assert status == 403
        assert "Nu ai permisiuni" in response.json["error"]

def test_role_required_not_logged_in(app):
    @role_required("admin")
    def protected():
        return "ok"

    with app.test_request_context():
        if "user" in session:
            session.pop("user")
        response = protected()
        assert response.status_code == 302
        assert "/login" in response.location

