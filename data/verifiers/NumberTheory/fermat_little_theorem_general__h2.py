import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mod_p(expr, p):
    if isinstance(expr, (int, sympy.Integer)):
        return (expr % p) == 0
    if isinstance(expr, float) or getattr(expr, 'is_Float', False):
        expr = sympy.Rational(expr)
    if isinstance(expr, sympy.Rational):
        n, d = expr.p, expr.q
        if d % p == 0:
            return False
        return (n % p) == 0
    if isinstance(expr, sympy.MatrixBase):
        return all(is_zero_mod_p(val, p) for val in expr)
    
    try:
        expr = sympy.simplify(expr)
    except Exception:
        pass

    if expr == 0:
        return True
        
    try:
        poly = sympy.poly(expr)
        for c in poly.coeffs():
            if not is_zero_mod_p(c, p):
                return False
        return True
    except Exception:
        try:
            return (expr % p) == 0
        except Exception:
            return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, p).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        a, p = witness
    except Exception:
        return [False, False]
        
    # Hypothesis 1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # Conclusion: a^p \equiv a \pmod p
    # Negated Conclusion: a^p \not\equiv a \pmod p
    try:
        if isinstance(a, (int, sympy.Integer)):
            is_equiv = (pow(int(a), int(p), int(p)) == int(a) % int(p))
            neg_q = not is_equiv
        else:
            ap = a**p
            diff = ap - a
            is_equiv = is_zero_mod_p(diff, p)
            neg_q = not is_equiv
    except Exception:
        # If a^p is undefined or cannot be computed, the equivalence fails.
        # However, to be safe and only accept valid mathematical objects as witnesses,
        # we return False if an exception occurs.
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: a^p is not equivalent to a mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1