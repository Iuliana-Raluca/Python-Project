from flask import Blueprint, request, jsonify
from .services import MathService
from .validators import Validator
from .models import db, OperationLog
from datetime import datetime, timezone

bp = Blueprint("routes", __name__)


@bp.route("/fibbo", methods=["GET", "POST"])
def fibonacci_route():
    try:
        if request.method == "POST":
            data = request.get_json()
            n = data.get("n")
            operation_str = request.path + " " + str(data)
        else:
            n = request.args.get("n", type=int)
            operation_str = request.path + "?" + request.query_string.decode()
        Validator.validate_positive_int(n)

        result = MathService.fibbo(n)
        status = 200

    except (ValueError, TypeError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500

    log = OperationLog(
        operation=operation_str,
        input_data=str(n),
        result=str(result),
        status_code=status,
        timestamp=datetime.now(timezone.utc)   
    )
    db.session.add(log)
    db.session.commit()

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status


@bp.route("/pow", methods=["GET", "POST"])
def pow_route():
    try:
        if request.method == "POST":
            data = request.get_json()
            a = data.get("a")
            b = data.get("b")
            operation_str = request.path + " " + str(data)
        else:
            a = request.args.get("a", type=int)
            b = request.args.get("b", type=int)
            operation_str = request.path + "?" + request.query_string.decode()

        Validator.validate_positive_int(a)
        Validator.validate_positive_int(b)

        result = MathService.pow(a, b)
        status = 200

    except (ValueError, TypeError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare internă: " + str(e)
        status = 500

    log = OperationLog(
        operation=operation_str,
        input_data=f"a={a}, b={b}",
        result=str(result),
        status_code=status,
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(log)
    db.session.commit()

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status


@bp.route("/factorial", methods=["GET", "POST"])
def factorial_route():
    try:
        if request.method == "POST":
            data = request.get_json()
            n = data.get("n")
            operation_str = request.path + " " + str(data)
        else:
            n = request.args.get("n", type=int)
            operation_str = request.path + "?" + request.query_string.decode()

        Validator.validate_positive_int(n)
        result = MathService.factorial(n)
        status = 200

    except (ValueError, TypeError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500

    log = OperationLog(
        operation=operation_str,
        input_data=str(n),
        result=str(result),
        status_code=status,
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(log)
    db.session.commit()

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status
