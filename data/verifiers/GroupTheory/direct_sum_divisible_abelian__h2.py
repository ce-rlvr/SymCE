import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_divisible_abelian(G):
    try:
        if not G.is_abelian:
            return False
        if hasattr(G, 'is_divisible'):
            return bool(G.is_divisible)
        # For finite groups, only the trivial group is divisible
        return G.order() == 1
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            groups = list(witness.values())
        else:
            groups = list(witness)
        h1 = True
    except Exception:
        h1 = False
        groups = []

    try:
        h2 = all(is_divisible_abelian(G) for G in groups) if groups else True
    except Exception:
        h2 = False

    try:
        if not h1 or not groups:
            neg_q = False
        else:
            # The direct sum of groups is divisible abelian iff all components are divisible abelian.
            is_ds_divisible = all(is_divisible_abelian(G) for G in groups)
            neg_q = not is_ds_divisible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: For every i in I, D_i is a divisible abelian group",
    "¬Q: The direct sum ⊕_{i ∈ I} D_i is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2