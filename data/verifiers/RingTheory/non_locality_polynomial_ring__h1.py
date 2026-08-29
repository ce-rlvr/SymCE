import sympy
from sympy import *
import itertools
import functools
import math

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = ["¬Q: The polynomial ring in one variable over R is a local ring"]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    neg_q = False
    try:
        if type(witness) is int:
            if witness in (0, 1):
                neg_q = True
        elif isinstance(witness, str):
            if witness.lower() in ["trivial ring", "zero ring", "0", "{0}", "z1", "z/1z"]:
                neg_q = True
        elif isinstance(witness, list):
            if witness == [0]:
                neg_q = True
        elif isinstance(witness, set):
            if witness == {0}:
                neg_q = True
        else:
            if hasattr(witness, 'is_zero') and witness.is_zero:
                neg_q = True
            elif hasattr(witness, 'zero') and hasattr(witness, 'one') and witness.zero == witness.one:
                neg_q = True
            elif witness == 0:
                neg_q = True
            elif witness == trivial:
                neg_q = True
    except Exception:
        pass

    return [bool(neg_q)]