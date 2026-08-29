import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def check_prop(witness, names):
    """
    Helper function to extract a boolean property from the witness.
    The witness can be a dictionary, an object, or a tuple (R, P).
    """
    args_to_try = [()]
    if isinstance(witness, (list, tuple)) and len(witness) == 2:
        R, P = witness
        args_to_try = [(R,), (P,), ()]
        objs = [witness, R, P]
    else:
        objs = [witness]
        
    for obj in objs:
        for name in names:
            if isinstance(obj, dict) and name in obj:
                val = obj[name]
            elif hasattr(obj, name):
                val = getattr(obj, name)
            else:
                continue
                
            if callable(val):
                success = False
                res = False
                for args in args_to_try:
                    try:
                        res = bool(val(*args))
                        success = True
                        break
                    except TypeError:
                        continue
                    except Exception:
                        continue
                if success:
                    return res
            else:
                return bool(val)
                
    raise AttributeError(f"None of {names} found")

def conditions(witness) -> list[bool]:
    # H_1: R has a multiplicative identity
    try:
        h1 = check_prop(witness, ['has_multiplicative_identity', 'has_identity', 'is_unital', 'identity'])
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    try:
        h2 = check_prop(witness, ['is_artinian', 'is_artinian_ring', 'artinian'])
    except Exception:
        h2 = False

    # H_3: P is a prime ideal of R
    try:
        h3 = check_prop(witness, ['is_prime_ideal', 'is_prime', 'prime_ideal', 'prime'])
    except Exception:
        h3 = False

    # ¬Q: P is not a maximal ideal
    try:
        is_max = check_prop(witness, ['is_maximal_ideal', 'is_maximal', 'maximal_ideal', 'maximal'])
        neg_q = not is_max
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "H_3: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3