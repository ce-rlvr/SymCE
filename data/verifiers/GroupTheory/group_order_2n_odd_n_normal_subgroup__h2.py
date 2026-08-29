import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is a finite group
    try:
        is_group = getattr(witness, 'is_group', False) or isinstance(witness, PermutationGroup)
        if is_group:
            order = witness.order()
            h1 = (order > 0) and (order != float('inf')) and (order != sympy.oo)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: The order of G is exactly 2n (which implies the order is even)
    try:
        if h1:
            h2 = (order % 2 == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G does NOT contain a normal subgroup of order n
    # Since |G| = 2n, a subgroup of order n has index 2.
    # Any subgroup of index 2 is normal.
    # A finite group has a subgroup of index 2 if and only if its abelianization (G/G') has even order.
    try:
        if h1 and h2:
            if hasattr(witness, 'derived_subgroup'):
                D = witness.derived_subgroup()
                abelianization_order = order // D.order()
                neg_q = (abelianization_order % 2 != 0)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is exactly 2n (even)",
    "¬Q: G does not contain a normal subgroup of order n"
]

N_HYP = 2
NEG_Q_INDEX = 2