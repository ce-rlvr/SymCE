import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: The commutator subgroup is a subgroup of N
    try:
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = G.derived_subgroup().is_subgroup(N)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The quotient group G/N is not abelian
    try:
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            if not N.is_subgroup(G):
                neg_q = True
            elif not N.is_normal(G):
                neg_q = True
            else:
                neg_q = not G.derived_subgroup().is_subgroup(N)
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: The commutator subgroup is a subgroup of N", "not Q: The quotient group G/N is not abelian"]

N_HYP = 2
NEG_Q_INDEX = 2