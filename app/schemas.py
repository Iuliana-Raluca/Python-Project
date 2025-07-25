from pydantic import BaseModel, ValidationError

class FibonacciInput(BaseModel):
    n: int

class PowInput(BaseModel):
    a: int
    b: int

class FactorialInput(BaseModel):
    n: int
