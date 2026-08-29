import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: Z(G) is the center of G (implicitly requires witness to be a group)
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # H_2: The quotient group G/Z(G) is abelian
        # G/Z(G) is abelian iff the commutator subgroup G' is a subgroup of Z(G)
        if not isinstance(witness, PermutationGroup):
            h2 = False
        else:
            Z = witness.center()
            G_prime = witness.derived_subgroup()
            h2 = bool(all(g in Z for g in G_prime.generators))
    except Exception:
        h2 = False

    try:
        # ¬Q: The commutator subgroup G' is NOT a subgroup of the center Z(G)
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            Z = witness.center()
            G_prime = witness.derived_subgroup()
            neg_q = not bool(all(g in Z for g in G_prime.generators))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: The quotient group G/Z(G) is abelian",
    "¬Q: The commutator subgroup G' is not a subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2