
from pydantic import ValidationError
from .schemas import FactorialInput, FibonacciInput, PowInput
from flask import Blueprint, request, jsonify, render_template
from .services import MathService
from .validators import Validator
from datetime import datetime, timezone
import asyncio
from .validators import require_api_key
from flask import redirect, flash, url_for
from app.models import User
from app import db
from functools import wraps
from flask_login import login_required, current_user, login_user
from flask import session
from flask import current_app
import aiosqlite


bp = Blueprint("routes", __name__, template_folder="../templates")


async def async_log_operation(operation, input_data, result, status_code, timestamp):
    await asyncio.sleep(2)
    db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]

    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "")
    else:
        raise ValueError("Unsupported DB URI")

    query = """
        INSERT INTO operation_log
        (operation, input_data, result, status_code, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """

    async with aiosqlite.connect(db_path) as db:
        await db.execute(query, (operation, input_data, result, status_code, timestamp))
        await db.commit()


@bp.route("/")
def root():
    return redirect(url_for("routes.register"))


@bp.route("/home")
def index():
    return render_template("index.html")


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html', role=current_user.role, username=current_user.username)


@bp.route("/fibbo", methods=["GET", "POST"])
async def fibonacci_route():
    operation_str = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            try:
                input_data = FibonacciInput(**data)
                n = input_data.n
            except ValidationError as e:
                return jsonify({'error': e.errors()}), 400
            operation_str = request.path + " " + str(data)
        else:
            n = request.args.get("n", type=int)
            operation_str = request.path + "?" + request.query_string.decode()
        n_valid = Validator.validate_positive_int(n, operation="fibonacci")
        if n_valid > Validator.MAX_VALUES["fibonacci"]:
            raise ValueError(
                f"Valoarea este prea mare pentru operatia Fibonacci. "
                f"Limita este {Validator.MAX_VALUES['fibonacci']}"
                )
        result = Validator.safe_math_call(MathService.fibbo, n_valid)
        status = 200
    except (ValueError, OverflowError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500
    try:
        await async_log_operation(
            operation_str,
            str(n) if 'n' in locals() else "",
            str(result),
            status,
            datetime.now(timezone.utc).isoformat()
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status


@bp.route('/pow', methods=['POST'])
async def pow_route():
    operation_str = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            try:
                input_data = PowInput(**data)
                a = input_data.a
                b = input_data.b
            except ValidationError as e:
                return jsonify({'error': e.errors()}), 400
            operation_str = request.path + " " + str(data)
        else:
            a = request.args.get("a", type=int)
            b = request.args.get("b", type=int)
            operation_str = request.path + "?" + request.query_string.decode()
        Validator.validate_positive_int(a, operation="pow")
        Validator.validate_positive_int(b, operation="pow")
        result = Validator.safe_math_call(MathService.pow, a, b)
        status = 200

    except (ValueError, OverflowError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare internă: " + str(e)
        status = 500

    await async_log_operation(
        operation_str,
        f"a={a}, b={b}",
        str(result),
        status,
        datetime.now(timezone.utc).isoformat()
    )

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status


@bp.route("/factorial", methods=["GET", "POST"])
@require_api_key
async def factorial_route():
    operation_str = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            try:
                input_data = FactorialInput(**data)
                n = input_data.n
            except ValidationError as e:
                return jsonify({'error': e.errors()}), 400
            operation_str = request.path + " " + str(data)
        else:
            n = request.args.get("n", type=int)
            operation_str = request.path + "?" + request.query_string.decode()

        Validator.validate_positive_int(n, operation="factorial")
        if n > Validator.MAX_VALUES["factorial"]:
            raise ValueError(
                f"Valoarea este prea mare pentru operația factorial."
                f"Limita este {Validator.MAX_VALUES['factorial']}")
        result = Validator.safe_math_call(MathService.factorial, n)
        status = 200

    except (ValueError, OverflowError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500

    await async_log_operation(
        operation_str,
        str(n) if 'n' in locals() else "",
        str(result),
        status,
        datetime.now(timezone.utc).isoformat()
    )

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect("/dashboard")

        flash("Date greșite.")
        return redirect("/login")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if User.query.filter_by(username=username).first():
            flash("Acest username există deja.")
            return redirect("/register")

        user = User(username=username, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash("Cont creat cu succes. Te poți autentifica.")
        return redirect("/login")

    return render_template("register.html")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user" not in session or session["user"]["role"] != role:
                return "Acces interzis.", 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Nu aveți permisiuni pentru a accesa această pagină.")
            return redirect(url_for("routes.dashboard"))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/loguri')
async def loguri():
    from flask_login import current_user
    from flask import redirect, url_for
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('routes.dashboard'))

    from flask import current_app

    db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")

    query = (
        "SELECT id, operation, input_data, result, status_code, timestamp "
        "FROM operation_log ORDER BY id DESC LIMIT 100"
    )
    logs = []
    import aiosqlite
    async with aiosqlite.connect(db_path) as db:
        async with db.execute(query) as cursor:
            async for row in cursor:
                logs.append({
                    'id': row[0],
                    'operation': row[1],
                    'input_data': row[2],
                    'result': row[3],
                    'status_code': row[4],
                    'timestamp': row[5]
                })
    return render_template('loguri.html', logs=logs)
