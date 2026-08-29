import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        if isinstance(witness, dict):
            H = witness.get('H')
            K = witness.get('K')
            G = witness.get('G')
        else:
            H, K, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(H, PermutationGroup) and bool(H.is_solvable)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(K, PermutationGroup) and bool(K.is_solvable)
    except Exception:
        h2 = False

    try:
        neg_q = isinstance(G, PermutationGroup) and not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite solvable group",
    "H_2: K is a finite solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2