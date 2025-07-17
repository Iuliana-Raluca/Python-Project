from flask import Blueprint, request, jsonify
from .services import MathService
from .validators import Validator
from .models import db, OperationLog

bp = Blueprint("routes", __name__)

@bp.route("/fibbo", methods=["GET", "POST"])
def fibonacci_route():
    try:
        if request.method == "POST":
            data = request.get_json()
            n = data.get("n")
        else:
            n = request.args.get("n", type=int)
        
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
        operation="fibbo",
        input_data=str(n),
        result=str(result),
        status_code=status 
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
            n = data.get("n")
        else:
            n = request.args.get("n", type=int)
            
        Validator.validate_positive_int(n)
        result = MathService.pow(n)
        status = 200

    except (ValueError, TypeError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500

    log = OperationLog(
        operation="pow",
        input_data=str(n),
        result=str(result),
        status_code=status
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
        else:
            n = request.args.get("n", type=int)

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
        operation="factorial",
        input_data=str(n),
        result=str(result),
        status_code=status
    )
    db.session.add(log)
    db.session.commit()

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": result}), status
