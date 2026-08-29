import math
import itertools
import functools
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3

def conditions(witness):
    try:
        # Witness should be a tuple or list of three numbers (x, y, z)
        if len(witness) != 3:
            return [False, False]
        x, y, z = witness
    except Exception:
        return [False, False]
        
    try:
        # Check if x^2 + y^2 + z^2 = 2xyz
        # We use sympy.simplify to correctly handle symbolic or irrational witnesses
        diff = sympy.simplify(x**2 + y**2 + z**2 - 2*x*y*z)
        h1 = (diff == 0)
    except Exception:
        h1 = False
        
    try:
        # Check negated conclusion: x, y, z are not all zero
        x_zero = (sympy.simplify(x) == 0)
        y_zero = (sympy.simplify(y) == 0)
        z_zero = (sympy.simplify(z) == 0)
        neg_q = not (x_zero and y_zero and z_zero)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x^2 + y^2 + z^2 = 2xyz",
    "¬Q: x, y, and z are not all zero"
]

N_HYP = 1
NEG_Q_INDEX = 1