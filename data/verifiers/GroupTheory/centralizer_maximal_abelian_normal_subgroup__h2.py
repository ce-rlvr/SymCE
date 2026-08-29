import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, A = witness
    except Exception:
        return [False, False]

    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # ¬Q: The centralizer of A in G is not equal to A
    try:
        A_elements = set(A.elements) if hasattr(A, 'elements') else set(A)
        A_gens = A.generators if hasattr(A, 'generators') else A_elements

        cent = set()
        for g in G.elements:
            commutes = True
            for a in A_gens:
                if g * a != a * g:
                    commutes = False
                    break
            if commutes:
                cent.add(g)

        neg_q = (cent != A_elements)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The centralizer of A in G is not equal to A"
]

N_HYP = 1
NEG_Q_INDEX = 1