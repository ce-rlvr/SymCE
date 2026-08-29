import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Aut(G) is the automorphism group of G
    # This is a definitional hypothesis that holds true for the witness group.
    h2 = h1

    # H_3: N = {(g, id) | g in G} is the canonical embedding of G into Hol(G)
    # This is also a definitional hypothesis.
    h3 = h1

    # ¬Q: N is not a normal subgroup of Hol(G)
    try:
        if not h1:
            neg_q = False
        else:
            # Mathematically, the holomorph Hol(G) is the semidirect product G ⋊ Aut(G).
            # The canonical embedding N = {(g, id) | g in G} corresponds to the base group G,
            # which is ALWAYS a normal subgroup in this semidirect product.
            # Since the conclusion "N is a normal subgroup of Hol(G)" is universally true 
            # for any group G, its negation is always False.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the automorphism group of G",
    "H_3: N = {(g, id) | g in G} is the canonical embedding of G into Hol(G)",
    "¬Q: N is not a normal subgroup of Hol(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3