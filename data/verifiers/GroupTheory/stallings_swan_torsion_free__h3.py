import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness):
    # H_1: G is a finitely generated group
    try:
        # In SymPy, PermutationGroup and FpGroup are finitely generated
        h1 = hasattr(witness, 'generators') and len(witness.generators) >= 0
    except Exception:
        h1 = False

    # H_2: G is virtually free
    try:
        h2 = False
        # A finite group is always virtually free because the trivial subgroup 
        # is a free group (of rank 0) and has finite index in G.
        if hasattr(witness, 'order'):
            ord_w = witness.order()
            if ord_w < float('inf'):
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is not a free group
    try:
        neg_q = False
        if hasattr(witness, 'order'):
            ord_w = witness.order()
            # A finite group is free if and only if it is the trivial group (order 1)
            if ord_w < float('inf'):
                neg_q = bool(ord_w > 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G is virtually free",
    "¬Q: G is not a free group"
]

N_HYP = 2
NEG_Q_INDEX = 2