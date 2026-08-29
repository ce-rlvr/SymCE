import sympy
from sympy.ntheory import jacobi_symbol
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: a is an integer",
    "¬Q: The Jacobi symbol (ab/n) does not equal (a/n)(b/n)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_integer(x):
    try:
        # Check if x is numerically equal to its integer conversion
        # This handles int, float (e.g., 2.0), and sympy.Integer/Rational
        return int(x) == x
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            n = witness.get('n')
        else:
            a, b, n = witness
    except Exception:
        return [False, False, False]

    # H_1: n is an odd positive integer
    try:
        h1 = is_integer(n) and n > 0 and int(n) % 2 == 1
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = is_integer(a)
    except Exception:
        h2 = False

    # ¬Q: (ab/n) != (a/n)(b/n)
    try:
        ab = a * b
        if is_integer(ab):
            ab = int(ab)
            
        n_int = int(n) if is_integer(n) else n
        a_int = int(a) if is_integer(a) else a
        b_val = int(b) if is_integer(b) else b
        
        lhs = jacobi_symbol(ab, n_int)
        rhs = jacobi_symbol(a_int, n_int) * jacobi_symbol(b_val, n_int)
        
        neg_q = bool(lhs != rhs)
    except Exception:
        # If evaluating the Jacobi symbol fails (e.g., because b is not an integer),
        # then the conclusion "(ab/n) equals (a/n)(b/n)" is considered to fail.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]