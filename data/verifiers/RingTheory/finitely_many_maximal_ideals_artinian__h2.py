import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import QQ, ZZ
from sympy.abc import x, y, z

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
    # H_1: R is a commutative ring
    h1 = False
    try:
        if hasattr(witness, 'is_commutative'):
            val = witness.is_commutative() if callable(witness.is_commutative) else witness.is_commutative
            h1 = bool(val)
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    h2 = False
    try:
        if hasattr(witness, 'is_artinian'):
            val = witness.is_artinian() if callable(witness.is_artinian) else witness.is_artinian
            h2 = bool(val)
    except Exception:
        h2 = False

    # ¬Q: R has infinitely many maximal ideals (negation of finitely many)
    neg_q = False
    try:
        if hasattr(witness, 'has_finitely_many_maximal_ideals'):
            val = witness.has_finitely_many_maximal_ideals() if callable(witness.has_finitely_many_maximal_ideals) else witness.has_finitely_many_maximal_ideals
            neg_q = not bool(val)
        elif hasattr(witness, 'has_infinitely_many_maximal_ideals'):
            val = witness.has_infinitely_many_maximal_ideals() if callable(witness.has_infinitely_many_maximal_ideals) else witness.has_infinitely_many_maximal_ideals
            neg_q = bool(val)
        elif hasattr(witness, 'maximal_ideals'):
            val = witness.maximal_ideals() if callable(witness.maximal_ideals) else witness.maximal_ideals
            if val == "infinite" or val == float('inf'):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "¬Q: R has infinitely many maximal ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2