import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is abelian
    try:
        if not h1:
            h2 = False
        else:
            Z = witness.center()
            h2 = True
            for g in witness.generators:
                for h in witness.generators:
                    comm = (~g) * (~h) * g * h
                    if comm not in Z:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The commutator subgroup G' is not a subgroup of the center Z(G)
    try:
        if not h1:
            neg_q = False
        else:
            Z = witness.center()
            G_prime = witness.derived_subgroup()
            neg_q = not all((g in Z) for g in G_prime.generators)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is abelian",
    "¬Q: The commutator subgroup G' is not a subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2