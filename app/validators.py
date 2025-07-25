from functools import wraps
from flask import request, jsonify, current_app


def require_api_key(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if api_key != current_app.config["API_KEY"]:
            return jsonify({"error": "Cheie API lipsa sau invalida."}), 401
        return await f(*args, **kwargs)
    return decorated


class Validator:
    @staticmethod
    def safe_math_call(func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None or (isinstance(result, float) and (result == float('inf') or result == float('-inf'))):
                raise ValueError("Rezultatul este prea mare sau nu poate fi calculat corect.")
            if not isinstance(result, int):
                raise ValueError("Rezultatul nu este un intreg valid.")
            return result
        except (OverflowError, ValueError) as e:
            raise ValueError(f"Eroare de calcul: {str(e)}")
    MAX_VALUES = {
        "factorial": 500,
        "pow": 10000,
        "fibonacci": 1000
    }

    @staticmethod
    def validate_positive_int(value, operation=None):
        # MODIFICARE: returnează valoarea validată (int)
        if isinstance(value, str):
            if value.isdigit():
                value = int(value)
            else:
                raise ValueError("Valoarea trebuie sa fie un intreg pozitiv.")
        if not isinstance(value, int):
            raise ValueError("Valoarea trebuie sa fie un intreg.")
        if value < 0:
            raise ValueError("Valoarea trebuie sa fie pozitiva.")
        if operation and value > Validator.MAX_VALUES.get(operation, 100000):
            raise ValueError(f"Valoarea este prea mare pentru operatia {operation}. Limita este {Validator.MAX_VALUES[operation]}")
        return value
