class MathService:
    @staticmethod
    def factorial(n: int) -> int:
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
    @staticmethod
    def pow(n: int) -> int:
        if n==1:
            return 1
        else:
            return n**n
        
    @staticmethod 
    def fibbo(n: int) -> int:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b