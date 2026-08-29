import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    # H_1: G is isomorphic to a direct product of non-abelian simple groups
    # A finite group is a direct product of non-abelian simple groups if and only if 
    # all of its composition factors are non-abelian simple groups.
    # A simple group is non-abelian if and only if its order is not a prime.
    h1 = False
    try:
        if hasattr(witness, "order") and hasattr(witness, "composition_series"):
            if witness.order() == 1:
                h1 = True
            else:
                comps = witness.composition_series()
                h1 = True
                for i in range(len(comps) - 1):
                    factor_order = comps[i].order() // comps[i+1].order()
                    if sympy.isprime(factor_order):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: The commutator subgroup [G, G] is not equal to G
    neg_q = False
    try:
        if hasattr(witness, "order") and hasattr(witness, "derived_subgroup"):
            neg_q = witness.derived_subgroup().order() != witness.order()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: G is isomorphic to a direct product of non-abelian simple groups", "neg_Q: The commutator subgroup of G is not equal to G"]

N_HYP = 1
NEG_Q_INDEX = 1