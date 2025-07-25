from pydantic import ValidationError
from .schemas import FactorialInput, FibonacciInput, PowInput
from flask import Blueprint, request, jsonify, render_template
from .services import MathService
from .validators import Validator
from datetime import datetime, timezone
import asyncio
import aiosqlite
from .validators import require_api_key


bp = Blueprint("routes", __name__, template_folder="../templates")

async def async_log_operation(operation, input_data, result, status_code, timestamp):
    await asyncio.sleep(2)
    db_path = r"C:\Users\iubutnariu\Desktop\Materiale\Python Project\flask_microservice\instance\database.db" 
    query = """
        INSERT INTO operation_log (operation, input_data, result, status_code, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(query, (operation, input_data, result, status_code, timestamp))
        await db.commit()

@bp.route("/home")
def index():
    return render_template("index.html")

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
        Validator.validate_positive_int(n, operation="fibonacci")
        result = Validator.safe_math_call(MathService.fibbo, n)
        status = 200

    except (ValueError, TypeError) as e:
        result = str(e)
        status = 400
    except Exception as e:
        result = "Eroare interna: " + str(e)
        status = 500

    await async_log_operation(
        operation_str,
        str(n),
        str(result),
        status,
        datetime.now(timezone.utc).isoformat()
    )

    if status == 200:
        return jsonify({"result": result}), 200
    else:
        Validator.validate_positive_int(n, operation="factorial")
        if n > Validator.MAX_VALUES["factorial"]:
            raise ValueError(f"Valoarea este prea mare pentru operația factorial. Limita este {Validator.MAX_VALUES['factorial']}")
        result = Validator.safe_math_call(MathService.factorial, n)
        status = 200
@bp.route("/pow", methods=["GET", "POST"])
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

    except (ValueError, TypeError) as e:
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
            raise ValueError(f"Valoarea este prea mare pentru operația factorial. Limita este {Validator.MAX_VALUES['factorial']}")
        result = Validator.safe_math_call(MathService.factorial, n)
        status = 200

    except (ValueError, TypeError) as e:
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
