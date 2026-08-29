import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains.domain import Domain
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

def get_bool(witness, *keys, default=False):
    """Helper to safely extract boolean properties from a dictionary or object."""
    if isinstance(witness, dict):
        for k in keys:
            if k in witness:
                return bool(witness[k])
        return default
    else:
        for k in keys:
            if hasattr(witness, k):
                try:
                    attr = getattr(witness, k)
                    return bool(attr() if callable(attr) else attr)
                except Exception:
                    pass
        return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    Since the conjecture is actually a true theorem (in a commutative Noetherian ring, 
    the nilradical is always nilpotent), no valid mathematical object can serve as a 
    counterexample. This verifier uses duck-typing to evaluate mock objects or dictionaries.
    """
    # Fast path for standard SymPy domains (which are commutative rings with identity)
    if isinstance(witness, Domain):
        # SymPy domains (like QQ, ZZ) are Noetherian and their nilradical is {0} (nilpotent)
        return [True, True, False]
        
    # H_1: R is a commutative ring with identity
    try:
        if isinstance(witness, dict) and 'is_commutative_with_identity' in witness:
            h1 = get_bool(witness, 'is_commutative_with_identity')
        elif hasattr(witness, 'is_commutative_with_identity'):
            h1 = get_bool(witness, 'is_commutative_with_identity')
        else:
            h1 = get_bool(witness, 'is_commutative') and get_bool(witness, 'has_identity')
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        h2 = get_bool(witness, 'is_noetherian')
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a positive integer k such that N^k = {0}
    # (i.e., the nilradical is NOT nilpotent)
    try:
        is_nilp = get_bool(witness, 'is_nilradical_nilpotent', 'nilradical_nilpotent', 'nilradical_is_nilpotent', default=True)
        neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: There does not exist a positive integer k such that N^k = {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2