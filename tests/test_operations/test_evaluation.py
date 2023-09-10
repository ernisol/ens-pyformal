from ens_pyformal.operations.operators import Multiply, Sum, Divide
from ens_pyformal.operations.functions import Sin, Cos
from ens_pyformal.operations.generic import Variable
import numpy as np
import math


def test_cos():
    x = Variable(name="x")
    fun = Cos(children=[x])
    assert fun.evaluate(x=10) == np.cos(10)


def test_sin():
    x = Variable(name="x")
    fun = Sin(children=[x])
    assert fun.evaluate(x=10) == np.sin(10)


def test_sum():
    inputs = {}
    children = []
    for i, var in enumerate("abcdefg"):
        children.append(Variable(name=var))
        inputs[var] = i + 1
    fun = Sum(children=children)
    assert fun.evaluate(**inputs) == 28


def test_multiply():
    inputs = {}
    children = []
    for i, var in enumerate("abcdefg"):
        children.append(Variable(name=var))
        inputs[var] = i + 1
    fun = Multiply(children=children)
    assert fun.evaluate(**inputs) == math.factorial(7)


def test_divide():
    vars = ["x", "y"]
    values = 7, 3
    fun = Divide(children=[Variable(name=name) for name in vars])
    assert fun.evaluate(**dict(zip(vars, values))) == 7 / 3
