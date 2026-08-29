import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    I = witness
    radical_func = None

    if isinstance(witness, tuple):
        if len(witness) == 2:
            if callable(witness[1]):
                I, radical_func = witness
            else:
                I = witness[0]
        elif len(witness) == 3:
            I = witness[0]
            if callable(witness[2]):
                radical_func = witness[2]

    h1 = False
    try:
        if hasattr(I, 'is_ideal'):
            val = I.is_ideal
            h1 = bool(val() if callable(val) else val)
        elif hasattr(I, 'is_ideal_of'):
            if isinstance(witness, tuple) and len(witness) >= 2 and not callable(witness[1]):
                h1 = bool(I.is_ideal_of(witness[1]))
        elif type(I).__name__ == 'Ideal':
            h1 = True
        else:
            from sympy.polys.agca.ideals import Ideal
            if isinstance(I, Ideal):
                h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if radical_func is not None:
            rad_I = radical_func(I)
            rad_rad_I = radical_func(rad_I)
            neg_q = bool(rad_rad_I != rad_I)
        elif hasattr(I, 'radical'):
            rad_I = I.radical() if callable(I.radical) else I.radical
            rad_rad_I = rad_I.radical() if callable(rad_I.radical) else rad_I.radical
            neg_q = bool(rad_rad_I != rad_I)
        elif hasattr(I, 'rad'):
            rad_I = I.rad() if callable(I.rad) else I.rad
            rad_rad_I = rad_I.rad() if callable(rad_I.rad) else rad_I.rad
            neg_q = bool(rad_rad_I != rad_I)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The radical of the radical of I is not equal to the radical of I"
]

N_HYP = 1
NEG_Q_INDEX = 1