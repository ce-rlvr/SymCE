import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]

    def apply_phi(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2:
            h3 = True
            for g in G.elements:
                val = apply_phi(phi, g)
                if val not in H.elements:
                    h3 = False
                    break
            
            if h3:
                for x in G.elements:
                    for y in G.elements:
                        xy = x * y
                        val_xy = apply_phi(phi, xy)
                        val_x = apply_phi(phi, x)
                        val_y = apply_phi(phi, y)
                        if val_xy != val_x * val_y:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2:
            id_H = H.identity
            for g in G.elements:
                if apply_phi(phi, g) != id_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a finite group",
    "H_3: phi is a group homomorphism from G to H",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3