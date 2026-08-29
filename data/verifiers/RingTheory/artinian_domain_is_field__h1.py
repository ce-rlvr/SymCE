import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import z3
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "If R has a multiplicative identity, is an Artinian ring, and is an integral domain, then R is a field."
    (The dropped hypothesis from the true theorem is that R is commutative).
    """
    def check_attr(obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                try:
                    return bool(val() if callable(val) else val)
                except Exception:
                    pass
            elif isinstance(obj, dict) and attr in obj:
                val = obj[attr]
                try:
                    return bool(val() if callable(val) else val)
                except Exception:
                    pass
        return None

    # H_1: R has a multiplicative identity
    try:
        h1 = check_attr(witness, ['has_multiplicative_identity', 'has_identity', 'is_unital'])
        h1 = False if h1 is None else h1
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    try:
        h2 = check_attr(witness, ['is_artinian', 'is_Artinian'])
        h2 = False if h2 is None else h2
    except Exception:
        h2 = False

    # H_3: R is an integral domain
    try:
        h3 = check_attr(witness, ['is_integral_domain', 'is_domain', 'is_IntegralDomain', 'has_no_zero_divisors'])
        h3 = False if h3 is None else h3
    except Exception:
        h3 = False

    # ¬Q: R is NOT a field
    try:
        q = check_attr(witness, ['is_field', 'is_Field'])
        neg_q = not q if q is not None else False
    except Exception:
        neg_q = False

    # Hardcoded fallback for known valid string counterexamples (e.g., non-commutative division rings)
    if isinstance(witness, str):
        w_lower = witness.lower().strip()
        if w_lower in ['quaternions', 'quaternion', 'h', 'mathbb{h}', 'division ring', 'non-commutative division ring']:
            h1, h2, h3, neg_q = True, True, True, True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "H_3: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3