import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation

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
    # H_1: G is a finite group
    try:
        ord_val = witness.order
        if callable(ord_val):
            ord_val = ord_val()
        h1 = (ord_val > 0) and (ord_val < float('inf'))
    except Exception:
        h1 = False

    # H_2: G is not a nilpotent group
    try:
        nilp = witness.is_nilpotent
        if callable(nilp):
            nilp = nilp()
        h2 = not nilp
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        solv = witness.is_solvable
        if callable(solv):
            solv = solv()
        neg_q = not solv
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is not a nilpotent group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2