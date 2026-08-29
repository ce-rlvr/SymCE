import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        H_1 = isinstance(witness, PermutationGroup)
    except Exception:
        H_1 = False

    try:
        G = witness
        G_prime = G.derived_subgroup()
        
        is_abelian = True
        for x in G.generators:
            for y in G.generators:
                commutator = (~x) * (~y) * x * y
                if commutator not in G_prime:
                    is_abelian = False
                    break
            if not is_abelian:
                break
                
        neg_Q = not is_abelian
    except Exception:
        neg_Q = False

    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The quotient group G/G' is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1