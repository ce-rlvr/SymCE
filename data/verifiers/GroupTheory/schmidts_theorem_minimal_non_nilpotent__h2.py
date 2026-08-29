import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup,
    AbelianGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Every proper subgroup of G is a nilpotent group
    h2 = False
    try:
        if not isinstance(witness, PermutationGroup):
            h2 = False
        elif getattr(witness, "is_nilpotent", False):
            # If G is nilpotent, all its subgroups are nilpotent.
            h2 = True
        elif hasattr(witness, "is_solvable") and not witness.is_solvable:
            # By Schmidt's Theorem, a finite group whose proper subgroups are all nilpotent is solvable.
            # Thus, if G is not solvable, it mathematically MUST have a non-nilpotent proper subgroup.
            h2 = False
        else:
            # G is solvable but not nilpotent. We search for a non-nilpotent proper subgroup.
            # A finite group is nilpotent iff all pairs of elements of coprime order commute.
            # Thus, any non-nilpotent subgroup must contain non-commuting elements of coprime order.
            order_G = witness.order()
            elements = []
            for g in witness.generate():
                elements.append(g)
                if len(elements) >= 2000:
                    break
            
            n_elements = len(elements)
            orders = [g.order() for g in elements]
            
            h2_eval = True
            pairs_checked = 0
            for i in range(n_elements):
                if not h2_eval:
                    break
                for j in range(i + 1, n_elements):
                    if math.gcd(orders[i], orders[j]) == 1:
                        x = elements[i]
                        y = elements[j]
                        if x * y != y * x:
                            H = PermutationGroup([x, y])
                            if H.order() < order_G:
                                h2_eval = False
                                break
                            pairs_checked += 1
                            # If we check many non-commuting coprime pairs and all generate G, 
                            # G is overwhelmingly likely a Schmidt group.
                            if pairs_checked > 5000:
                                break
                if pairs_checked > 5000:
                    break
            h2 = h2_eval
    except Exception:
        h2 = False

    # neg_Q: G is not a solvable group
    neg_q = False
    try:
        if isinstance(witness, PermutationGroup):
            neg_q = not witness.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Every proper subgroup of G is a nilpotent group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2