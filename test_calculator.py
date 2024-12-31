import pytest
from calculator import Calculator

# def test_divide_by_zero():
#     calculator = Calculator()
#     with pytest.raises(ValueError, match="Cannot divide by zero"):
#         calculator.divide(5, 0)

# def test_divide_positive_numbers():
#     calculator = Calculator()
#     assert calculator.divide(10, 2) == 5

# def test_divide_negative_numbers():
#     calculator = Calculator()
#     assert calculator.divide(-10, -2) == 5

# def test_divide_positive_and_negative_numbers():
#     calculator = Calculator()
#     assert calculator.divide(-10, 2) == -5

# 

def test_multiply():
    calculator = Calculator()
    assert calculator.multiply(3, 4) == 12

def test_divide():
    calculator = Calculator()
    assert calculator.divide(10, 2) == 5

def test_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(10, 0)

