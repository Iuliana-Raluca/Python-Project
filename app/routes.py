from flask import Blueprint, request, jsonify
from .services import MathService
from .validators import Validator
from .models import db, OperationLog

bp = Blueprint("routes", __name__)

@bp.route("/fibbo", methods = ["POST"])
def fibbonaci():
    data = request.get_json()

    try:
        n = data.get("n")
        result = MathService.fibbo(n)

        log = OperationLog(
            operation = "fibbo",
            input_data = str(data),
            result = str(result)
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({ "result" : result}), 200
    

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    

@bp.route("/pow", methods=["POST"])
def pow_route():
    data = request.get_json()

    try:
        n=data.get("n")
        result = MathService.pow(n)

        log = OperationLog(
            operation = "pow",
            input_data = str(data),
            result = str(result)
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({"result" : result}), 200
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400



@bp.route("/factorial", methods=["POST"])
def factorial_route():
    data = request.get_json()

    try:
        n = data.get("n")
        Validator.validate_positive_int(n)

        result = MathService.factorial(n)

        log = OperationLog(
            operation="factorial",
            input_data=str(data),
            result=str(result)
        )
        db.session.add(log)

        db.session.commit()

        return jsonify({"result": result}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
