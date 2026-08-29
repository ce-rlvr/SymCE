import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

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

def conditions(witness) -> list[bool]:
    # Extract G and optionally p from the witness
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = None
            
        # H_1: G is a group
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        G = None
        p = None

    # H_2: The index of the center Z(G) in G is exactly p^2
    try:
        if not h1:
            h2 = False
        else:
            Z = G.center()
            idx = int(G.order()) // int(Z.order())
            if p is not None:
                h2 = (idx == int(p)**2)
            else:
                root = math.isqrt(idx)
                h2 = (root * root == idx) and idx > 0
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of the center Z(G) in G is exactly p^2",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2