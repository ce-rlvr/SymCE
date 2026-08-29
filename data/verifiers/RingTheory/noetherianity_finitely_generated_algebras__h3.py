import sympy
from sympy import ZZ, QQ

class AbstractRing:
    def __init__(self, name, is_commutative, is_noetherian, base_rings=None):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        self.base_rings = base_rings or []

    def is_algebra_over(self, other):
        if self == other:
            return True
        if getattr(other, 'name', '') == 'Z' or other == ZZ:
            return True
        return other in self.base_rings

    def __repr__(self):
        return self.name

# Top-level setup: named object bindings for the witness expression
Z = AbstractRing('Z', True, True)
Q = AbstractRing('Q', True, True, base_rings=[Z, ZZ])
R = AbstractRing('R', True, True, base_rings=[Z, ZZ, Q, QQ])
C = AbstractRing('C', True, True, base_rings=[Z, ZZ, Q, QQ, R])

# Polynomial rings in infinitely many variables (Standard counterexamples for non-Noetherian rings)
Z_inf = AbstractRing('Z[x1, x2, ...]', True, False, base_rings=[Z, ZZ])
Q_inf = AbstractRing('Q[x1, x2, ...]', True, False, base_rings=[Z, ZZ, Q, QQ])
R_inf = AbstractRing('R[x1, x2, ...]', True, False, base_rings=[Z, ZZ, Q, QQ, R])
C_inf = AbstractRing('C[x1, x2, ...]', True, False, base_rings=[Z, ZZ, Q, QQ, R, C])

# Non-commutative rings
Free_Q = AbstractRing('Q<x, y>', False, False, base_rings=[Z, ZZ, Q, QQ])

def is_comm(ring):
    if isinstance(ring, AbstractRing):
        return ring.is_commutative
    if hasattr(ring, 'is_commutative'):
        return ring.is_commutative
    return True

def is_noeth(ring):
    if isinstance(ring, AbstractRing):
        return ring.is_noetherian
    if ring in [ZZ, QQ]:
        return True
    return False

def is_alg(A, R_ring):
    if isinstance(A, AbstractRing):
        return A.is_algebra_over(R_ring)
    if R_ring == ZZ or getattr(R_ring, 'name', '') == 'Z':
        return True
    if A == R_ring:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        R_ring, A_ring = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = bool(is_comm(R_ring) and is_noeth(R_ring))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(is_comm(A_ring) and is_alg(A_ring, R_ring))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(is_noeth(A_ring))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: A is a commutative R-algebra",
    "¬Q: A is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2