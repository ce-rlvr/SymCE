import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
x, y = sympy.symbols('x y')

# The witness should be a tuple (f, g, z) representing a counterexample on the ring of sequences R^N.
# - f: a function mapping a sequence to a sequence (the surjective ring homomorphism)
# - g: a function mapping a sequence to a sequence (the right inverse of f, proving surjectivity)
# - z: a sequence (function from int to int) that is non-zero, but f(z) is zero (proving f is not injective)
# A sequence is represented as a Python function taking a non-negative integer index.

def conditions(witness) -> list[bool]:
    try:
        f, g, z = witness
    except Exception:
        return [False, False]
        
    # Test sequences to verify homomorphism and surjectivity properties
    s1 = lambda n: n + 1
    s2 = lambda n: n**2 + 2
    s_add = lambda n: s1(n) + s2(n)
    s_mul = lambda n: s1(n) * s2(n)
    s_one = lambda n: 1
    
    try:
        # H_1: f is a surjective ring homomorphism
        
        # 1. f is a ring homomorphism
        # f(s1 + s2) == f(s1) + f(s2)
        add_ok = all(f(s_add)(n) == f(s1)(n) + f(s2)(n) for n in range(50))
        # f(s1 * s2) == f(s1) * f(s2)
        mul_ok = all(f(s_mul)(n) == f(s1)(n) * f(s2)(n) for n in range(50))
        # f(1) == 1
        one_ok = all(f(s_one)(n) == 1 for n in range(50))
        
        # 2. f is surjective (g is a right inverse)
        surj_ok = (
            all(f(g(s1))(n) == s1(n) for n in range(50)) and
            all(f(g(s2))(n) == s2(n) for n in range(50))
        )
        
        h1_ok = bool(add_ok and mul_ok and one_ok and surj_ok)
    except Exception:
        h1_ok = False
        
    try:
        # ¬Q: f is not injective
        
        # z is not the zero sequence
        z_not_zero = any(z(n) != 0 for n in range(50))
        # f(z) is the zero sequence
        fz_is_zero = all(f(z)(n) == 0 for n in range(50))
        
        neg_q_ok = bool(z_not_zero and fz_is_zero)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism",
    "¬Q: f is not injective"
]

N_HYP = 1
NEG_Q_INDEX = 1