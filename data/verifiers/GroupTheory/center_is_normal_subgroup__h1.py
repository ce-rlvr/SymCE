import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "¬Q: Z(G) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, Z = witness
        else:
            G = witness
            Z = G.center()
    except Exception:
        return [False, False]

    try:
        actual_center = G.center()
        if hasattr(Z, 'is_subgroup'):
            h1 = bool(Z.is_subgroup(actual_center) and actual_center.is_subgroup(Z))
        elif hasattr(Z, 'elements') and hasattr(actual_center, 'elements'):
            h1 = set(Z.elements) == set(actual_center.elements)
        else:
            h1 = (Z == actual_center)
    except Exception:
        h1 = False

    try:
        if hasattr(Z, 'is_normal'):
            q = bool(Z.is_normal(G))
        else:
            q = True
            for g in G.elements:
                for z in Z.elements:
                    if (g * z * g**-1) not in Z.elements:
                        q = False
                        break
                if not q:
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]