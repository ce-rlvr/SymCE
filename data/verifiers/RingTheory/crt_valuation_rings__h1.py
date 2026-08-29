import sympy
from sympy import gcd, gcdex
import math
import itertools
import functools

# Top-level setup: named object bindings
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "For any ring R, if I and J are comaximal ideals, then either I = R or J = R."
    
    A valid witness is a tuple (i, j) or (R, i, j) representing the generators 
    of the principal ideals I = <i> and J = <j> in a commutative ring (e.g., ZZ or F[x]).
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, i, j = witness
            elif len(witness) == 2:
                i, j = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: I and J are ideals of R
    try:
        # We assume i and j are generators of the principal ideals I and J.
        # They must be valid elements of a commutative ring (integers or sympy expressions).
        valid_types = (int, sympy.Integer, sympy.Expr, sympy.Poly)
        h1_ok = isinstance(i, valid_types) and isinstance(j, valid_types)
    except Exception:
        h1_ok = False

    # H_2: I and J are comaximal
    try:
        # Comaximal means I + J = R, so there exist a, b such that a*i + b*j = 1 (or a unit).
        if isinstance(i, (int, sympy.Integer)) and isinstance(j, (int, sympy.Integer)):
            h2_ok = (abs(sympy.gcd(i, j)) == 1)
        else:
            # For polynomials, try gcdex to ensure Bezout's identity holds
            a, b, g = sympy.gcdex(i, j)
            if isinstance(g, (int, sympy.Integer)):
                h2_ok = (abs(g) == 1)
            elif isinstance(g, (sympy.Expr, sympy.Poly)):
                h2_ok = bool(g.is_constant() and g != 0)
            else:
                h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: Neither I = R nor J = R
    try:
        # I = R means the generator i is a unit.
        def is_unit(x):
            if isinstance(x, (int, sympy.Integer)):
                return abs(x) == 1
            elif isinstance(x, (sympy.Expr, sympy.Poly)):
                return bool(x.is_constant() and x != 0)
            return False
        
        neg_q_ok = not is_unit(i) and not is_unit(j)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I and J are comaximal",
    "¬Q: Neither I = R nor J = R"
]

N_HYP = 2
NEG_Q_INDEX = 2