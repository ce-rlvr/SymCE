import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import symbols, Rational, Integer

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

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            G = witness[0]
        else:
            G = witness
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (tuple, list)):
            G = witness[0]
        else:
            G = witness
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, (tuple, list)):
            G = witness[0]
        else:
            G = witness
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: N is the normal closure of L over K",
    "¬Q: N is not a radical extension of K (Galois group is not solvable)"
]

N_HYP = 2
NEG_Q_INDEX = 2