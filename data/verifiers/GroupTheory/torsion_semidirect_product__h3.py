import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            G = witness['G']
        elif hasattr(witness, 'N') and hasattr(witness, 'H'):
            N = witness.N
            H = witness.H
            G = witness
        else:
            N, H, G = witness
    except Exception:
        return [False, False, False]

    def has_finite_order(g):
        if hasattr(g, 'order'):
            try:
                from sympy import oo
                return g.order() < oo
            except Exception:
                pass
        if hasattr(g, 'is_Matrix') and g.is_Matrix:
            I = g.eye(g.rows)
            curr = g
            for k in range(1, 200):
                if curr == I:
                    return True
                curr = curr * g
            return False
        raise ValueError("Cannot determine if element has finite order")

    def is_torsion(grp):
        if hasattr(grp, 'is_torsion_group'):
            val = grp.is_torsion_group() if callable(grp.is_torsion_group) else grp.is_torsion_group
            return bool(val)
        if hasattr(grp, 'is_torsion'):
            val = grp.is_torsion() if callable(grp.is_torsion) else grp.is_torsion
            return bool(val)
        if hasattr(grp, 'order'):
            try:
                from sympy import oo
                if grp.order() < oo:
                    return True
            except Exception:
                pass
        if hasattr(grp, 'is_finite'):
            val = grp.is_finite() if callable(grp.is_finite) else grp.is_finite
            if val is True:
                return True
        if isinstance(grp, (list, tuple, set)):
            for g in grp:
                if not has_finite_order(g):
                    return False
            return True
        raise ValueError("Cannot determine if torsion group")

    try:
        h1 = is_torsion(N)
    except Exception:
        h1 = False

    try:
        h2 = is_torsion(H)
    except Exception:
        h2 = False

    try:
        neg_q = not is_torsion(G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a torsion group",
    "H_2: H is a torsion group",
    "¬Q: G is not a torsion group"
]

N_HYP = 2
NEG_Q_INDEX = 2