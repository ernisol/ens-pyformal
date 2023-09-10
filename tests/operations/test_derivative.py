from ens_pyformal.operations.operators import Multiply, Sum, Divide
from ens_pyformal.operations.functions import Sin, Cos
from ens_pyformal.operations.generic import Variable, Constant
import numpy as np
import math


def test_cos():
    x = Variable("x")
    fun = Cos(children=[x])
    derivative = fun.derivative(variable_name="x")
    assert derivative.evaluate(x=0) == 0
    assert abs(derivative.evaluate(x=np.pi/2) + 1) < 1e-9

def test_sin():
    x = Variable("x")
    fun = Sin(children=[x])
    derivative = fun.derivative(variable_name="x")
    assert derivative.evaluate(x=0) == 1
    assert abs(derivative.evaluate(x=np.pi/2)) < 1e-9

def test_linear():
    x = Variable("x")
    fun = Multiply(children=[Constant(2), x])
    derivative = fun.derivative(variable_name="x")
    assert derivative.evaluate(x=0) == 2
    assert derivative.evaluate(x=10) == 2
