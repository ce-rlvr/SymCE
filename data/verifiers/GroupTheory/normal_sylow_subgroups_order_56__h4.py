import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of G is 56
    try:
        h2 = h1 and witness.order() == 56
    except Exception:
        h2 = False

    # H_3: n_7 is the number of Sylow 7-subgroups of G
    # This is a definitional hypothesis; it holds trivially if G is a valid group of order 56.
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # ¬Q: n_7 != 1 and n_2 != 1
    try:
        if not h2:
            neg_q = False
        else:
            elements = list(witness.generate())
            
            # A Sylow 7-subgroup has order 7. If n_7 == 1, there is exactly 1 such subgroup,
            # which contains 6 elements of order 7. If n_7 > 1, there are 8 such subgroups,
            # containing 48 elements of order 7.
            count_7 = sum(1 for g in elements if g.order() == 7)
            n7_is_1 = (count_7 == 6)
            
            # A Sylow 2-subgroup has order 8. If n_2 == 1, there is exactly 1 such subgroup,
            # which contains 7 elements of order 2, 4, or 8. If n_2 > 1, the union of the 
            # Sylow 2-subgroups will contain strictly more than 7 such elements.
            count_2_4_8 = sum(1 for g in elements if g.order() in (2, 4, 8))
            n2_is_1 = (count_2_4_8 == 7)
            
            neg_q = (not n7_is_1) and (not n2_is_1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is 56",
    "H_3: n_7 is the number of Sylow 7-subgroups of G",
    "¬Q: n_7 != 1 and n_2 != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3