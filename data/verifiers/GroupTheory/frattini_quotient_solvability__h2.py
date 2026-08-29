import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H1: G is a finite group
    try:
        if isinstance(witness, PermutationGroup):
            h1 = True
        elif hasattr(witness, 'is_finite'):
            h1 = bool(witness.is_finite)
        elif hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            from sympy import oo
            h1 = order != oo and order != float('inf')
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: G/Phi(G) is a solvable group
    # Note: For finite groups, Frattini's theorem states that the Frattini subgroup Phi(G) 
    # is nilpotent and thus solvable. Since an extension of a solvable group by a solvable 
    # group is solvable, G/Phi(G) is solvable if and only if G is solvable.
    try:
        solv = witness.is_solvable
        if callable(solv):
            solv = solv()
        h2 = bool(solv)
    except Exception:
        h2 = False

    # neg_Q: The group G is NOT solvable
    try:
        solv = witness.is_solvable
        if callable(solv):
            solv = solv()
        neg_q = not bool(solv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G/Phi(G) is a solvable group",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2