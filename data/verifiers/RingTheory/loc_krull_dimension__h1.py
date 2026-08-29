import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebraic objects
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

def _extract_value(obj, keys):
    """Helper to extract a value from a mock object or dictionary."""
    if isinstance(obj, dict):
        for k in keys:
            if k in obj:
                val = obj[k]
                return val() if callable(val) else val
    else:
        for k in keys:
            if hasattr(obj, k):
                val = getattr(obj, k)
                return val() if callable(val) else val
    raise ValueError(f"None of the keys {keys} found in object")

def conditions(witness) -> list[bool]:
    """
    Given a witness object, evaluates the remaining hypotheses and the negated conclusion.
    Since dim(R_P) = ht(P) is a tautology for commutative rings, the counterexample must be 
    a non-commutative ring. SymPy does not natively support non-commutative localizations, 
    so the witness is expected to be a mock object or dictionary providing these properties.
    """
    h1_ok = False
    try:
        # Check if P is a prime ideal of R
        h1_ok = bool(_extract_value(witness, [
            'is_prime_ideal', 'is_prime', 'P_is_prime', 'is_prime_ideal_of_R'
        ]))
    except Exception:
        try:
            # Handle case where witness might be a tuple (R, P)
            if isinstance(witness, tuple) and len(witness) == 2:
                h1_ok = bool(_extract_value(witness[1], ['is_prime_ideal', 'is_prime']))
        except Exception:
            h1_ok = False

    neg_q_ok = False
    try:
        # Check if the Krull dimension of R_P is NOT equal to the height of P
        dim = _extract_value(witness, [
            'dim_R_P', 'krull_dimension_R_P', 'dim_localized', 
            'krull_dimension_of_localized_ring_R_P', 'dim_localized_ring',
            'krull_dimension'
        ])
        ht = _extract_value(witness, [
            'height_P', 'height', 'ht_P', 'height_of_P'
        ])
        neg_q_ok = (dim != ht)
    except Exception:
        try:
            if isinstance(witness, tuple) and len(witness) == 2:
                dim = _extract_value(witness[1], [
                    'dim_R_P', 'krull_dimension_R_P', 'dim_localized', 'krull_dimension'
                ])
                ht = _extract_value(witness[1], ['height', 'ht'])
                neg_q_ok = (dim != ht)
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: The Krull dimension of the localized ring R_P is not equal to the height of P"
]

N_HYP = 1
NEG_Q_INDEX = 1