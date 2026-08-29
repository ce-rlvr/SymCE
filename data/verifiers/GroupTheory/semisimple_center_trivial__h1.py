import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: The center of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: G is isomorphic to a direct product of non-abelian simple groups
    # For computationally feasible finite groups, this is equivalent to having no abelian composition factors.
    h1_ok = False
    try:
        if hasattr(witness, "order") and hasattr(witness, "composition_series"):
            if witness.order() == 1:
                h1_ok = True
            else:
                series = witness.composition_series()
                h1_ok = True
                for i in range(len(series) - 1):
                    factor_order = series[i].order() // series[i+1].order()
                    # Abelian simple groups have prime order.
                    # If any composition factor has prime order, it's not a direct product of non-abelian simple groups.
                    if isprime(factor_order):
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # neg_Q: The center of G is not the trivial subgroup
    neg_q_ok = False
    try:
        if hasattr(witness, "center"):
            neg_q_ok = witness.center().order() > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]