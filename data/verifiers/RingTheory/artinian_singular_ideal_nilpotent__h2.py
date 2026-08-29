import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
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
    try:
        if callable(witness):
            witness = witness()
    except Exception:
        pass

    def check_attr(obj, attr_names, default):
        if isinstance(obj, dict):
            for attr in attr_names:
                if attr in obj:
                    return obj[attr]
        for attr in attr_names:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        return val()
                    except TypeError:
                        try:
                            return val(obj)
                        except Exception:
                            pass
                return val
        return default

    h1 = False
    try:
        h1 = check_attr(witness, ['is_right_artinian', 'is_artinian'], False)
    except Exception:
        pass

    q = True
    try:
        q = check_attr(witness, [
            'is_Z_nilpotent', 
            'is_right_singular_ideal_nilpotent', 
            'right_singular_ideal_is_nilpotent', 
            'Z_is_nilpotent', 
            'is_singular_ideal_nilpotent'
        ], True)
    except Exception:
        pass

    return [bool(h1), not bool(q)]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: Z(R_R) is not a nilpotent ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1