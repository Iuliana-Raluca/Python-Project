import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services import MathService

# Teste pentru factorial

def test_factorial_basic():
    assert MathService.factorial(0) == 1
    assert MathService.factorial(1) == 1
    assert MathService.factorial(5) == 120

def test_factorial_large():
    assert MathService.factorial(20) == 2432902008176640000

# Teste pentru pow

def test_pow_basic():
    assert MathService.pow(5, 0) == 1

def test_pow_large_overflow():
    with pytest.raises(ValueError, match="Rezultatul a depasit limita maxima de reprezentare."):
        MathService.pow(10**308, 2)

def test_pow_force_overflowerror():
    huge = float('1e10000')  
    with pytest.raises(ValueError, match="Rezultatul este prea mare."):
        MathService.pow(huge, 2)


# Teste pentru fibbo

def test_fibbo_basic():
    assert MathService.fibbo(0) == 0
    assert MathService.fibbo(1) == 1
    assert MathService.fibbo(10) == 55

def test_fibbo_large():
    assert MathService.fibbo(30) == 832040




