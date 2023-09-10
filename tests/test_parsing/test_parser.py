from ens_pyformal.parsing.parser import parse
import numpy as np


def test_sum():
    equation = "a + b"
    parsed_equation = parse(equation=equation)
    assert parsed_equation.evaluate(a=1, b=2) == 3
    assert parsed_equation.derivative(variable_name="a").evaluate() == 1


def test_cos():
    equation = "cos(x)"
    parsed_equation = parse(equation=equation)
    assert parsed_equation.evaluate(x=0) == 1
    assert abs(parsed_equation.evaluate(x=np.pi / 2)) < 1e-9


def test_sin():
    equation = "sin(x)"
    parsed_equation = parse(equation=equation)
    assert parsed_equation.evaluate(x=0) == 0
    assert abs(parsed_equation.evaluate(x=np.pi / 2)) == 1


def test_various():
    equation = "sin(x + cos(10))"
    parsed_equation = parse(equation=equation)
    assert parsed_equation.evaluate(x=0) == np.sin(np.cos(10))
    assert abs(parsed_equation.evaluate(x=np.pi / 2)) == np.sin(np.pi / 2 + np.cos(10))
