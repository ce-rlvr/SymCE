import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: H is a proper subgroup of G
    try:
        h2 = bool(H.is_subgroup(G) and H.order() < G.order())
    except Exception:
        h2 = False

    # ¬Q: H is NOT strictly contained in its normalizer N_G(H)
    # This means there is no element in G \ H that normalizes H.
    try:
        strictly_contained = False
        for g in G.elements:
            if g not in H:
                normalizes = True
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        normalizes = False
                        break
                if normalizes:
                    strictly_contained = True
                    break
        neg_q = not strictly_contained
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: H is a proper subgroup of G",
    "¬Q: H is not strictly contained in its normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2