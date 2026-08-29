import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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

    # ¬Q: The center of G is not the trivial subgroup
    try:
        if not h1:
            neg_q = False
        else:
            try:
                # sympy's PermutationGroup has a center() method returning a subgroup
                c = witness.center()
                neg_q = c.order() > 1
            except AttributeError:
                # Fallback manual computation if center() is not available
                gens = witness.generators
                c_size = 0
                for g in witness.generate():
                    if all(g * h == h * g for h in gens):
                        c_size += 1
                        if c_size > 1:
                            break
                neg_q = c_size > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The center of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1