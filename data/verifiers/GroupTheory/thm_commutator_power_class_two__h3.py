import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
        if len(witness) == 4:
            G, x, y, n = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) or hasattr(G, 'generators')
    except Exception:
        h1_ok = False

    try:
        if hasattr(G, 'derived_subgroup') and hasattr(G, 'center'):
            derived = G.derived_subgroup()
            center = G.center()
            h2_ok = bool(derived.is_subgroup(center))
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool((x in G) and (y in G))
    except Exception:
        h3_ok = False

    try:
        def commutator(a, b):
            return (a**-1) * (b**-1) * a * b
        
        lhs = commutator(x**n, y)
        rhs = commutator(x, y)**n
        
        neg_q_ok = bool(lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: G is a group", "H_2: Commutator subgroup in center", "H_3: x and y in G", "not_Q: commutator power identity fails"]

N_HYP = 3
NEG_Q_INDEX = 3