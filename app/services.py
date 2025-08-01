import math
from functools import lru_cache


class MathService:
    @staticmethod
    @lru_cache(maxsize=512)
    def factorial(n: int) -> int:
        print(f"factorial({n})")
        try:
            result = math.factorial(n)
            return result
        except OverflowError:
            raise ValueError("Rezultatul factorialului este prea mare.")

    @staticmethod
    def pow(a: int, b: int) -> int:
        try:
            result = math.pow(a, b)
            if math.isinf(result):
                raise ValueError("Rezultatul este prea mare.")
            return int(result)
        except OverflowError:
            raise ValueError("Rezultatul a depasit limita maxima de reprezentare.")

    @staticmethod
    @lru_cache(maxsize=512)
    def fibbo(n: int) -> int:
        print(f"fibbo({n})")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
