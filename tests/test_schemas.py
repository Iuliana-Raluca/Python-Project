import pytest
from app.schemas import FibonacciInput, PowInput, FactorialInput
from pydantic import ValidationError

# FibonacciInput

def test_fibonacci_input_valid():
    data = FibonacciInput(n=10)
    assert data.n == 10

def test_fibonacci_input_invalid_type():
    with pytest.raises(ValidationError):
        FibonacciInput(n="abc")  # string invalid

# PowInput

def test_pow_input_valid():
    data = PowInput(a=2, b=5)
    assert data.a == 2
    assert data.b == 5

def test_pow_input_invalid_a():
    with pytest.raises(ValidationError):
        PowInput(a="not_a_number", b=5)

def test_pow_input_invalid_b():
    with pytest.raises(ValidationError):
        PowInput(a=2, b=None)

# FactorialInput

def test_factorial_input_valid():
    data = FactorialInput(n=6)
    assert data.n == 6

def test_factorial_input_missing_n():
    with pytest.raises(ValidationError):
        FactorialInput()  
