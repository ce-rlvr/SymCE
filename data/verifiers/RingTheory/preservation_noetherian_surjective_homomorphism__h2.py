import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively represent non-Noetherian rings (like polynomial rings 
# in infinitely many variables), we provide dummy objects for the witness to use.
class _DummyRing:
    def __init__(self, comm, noeth):
        self.is_commutative_ring = comm
        self.is_noetherian = noeth
        
    def __str__(self):
        return f"Ring(commutative={self.is_commutative_ring}, noetherian={self.is_noetherian})"

NonNoetherianRing = _DummyRing(True, False)
CommutativeRing = _DummyRing(True, True)

def is_commutative_ring(ring):
    if hasattr(ring, 'is_commutative_ring'):
        return ring.is_commutative_ring
    if hasattr(ring, 'get_ring'):
        return True
    s = str(ring)
    if s in ["Integers", "Rationals", "Reals", "Complexes", "ZZ", "QQ", "RR", "CC"]:
        return True
    if isinstance(ring, str):
        s = ring.lower()
        if "non-commutative" in s or "noncommutative" in s or "matrix" in s or "free" in s:
            return False
        return True
    return False

def is_noetherian(ring):
    if hasattr(ring, 'is_noetherian'):
        return ring.is_noetherian
    if hasattr(ring, 'get_ring'):
        return True
    s = str(ring)
    if s in ["Integers", "Rationals", "Reals", "Complexes", "ZZ", "QQ", "RR", "CC"]:
        return True
    if isinstance(ring, str):
        s = ring.lower()
        if "infinite" in s or "..." in s or "non-noetherian" in s or "nonnoetherian" in s:
            return False
        if "x1" in s and "x2" in s and "x3" in s:
            return False
        if "x_1" in s and "x_2" in s and "x_3" in s:
            return False
        return True
    return True

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be a tuple of two rings (R, S)),
    returns a list of booleans corresponding to the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            R, S = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let R and S be commutative rings
    try:
        h1_ok = bool(is_commutative_ring(R) and is_commutative_ring(S))
    except Exception:
        h1_ok = False

    # H_2: Let R be a Noetherian ring
    try:
        h2_ok = bool(is_noetherian(R))
    except Exception:
        h2_ok = False

    # ¬Q: The ring S is NOT a Noetherian ring
    try:
        neg_q_ok = not bool(is_noetherian(S))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: R is a Noetherian ring",
    "¬Q: S is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2