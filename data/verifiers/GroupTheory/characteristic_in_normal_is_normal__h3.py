import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects
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

def is_normal_subgroup(G, N):
    """Helper to check if N is a normal subgroup of G."""
    try:
        if not isinstance(N, PermutationGroup):
            return False
        # Check if N is a subgroup of G
        for gen in N.generators:
            if not G.contains(gen):
                return False
        # Check normality: g^-1 * n * g in N for all generators
        for g in G.generators:
            for n in N.generators:
                if not N.contains(~g * n * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            K = witness.get('K')
        else:
            G, N, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = is_normal_subgroup(G, N)
    except Exception:
        h2_ok = False

    # ¬Q: K is NOT a normal subgroup of G
    try:
        neg_q_ok = not is_normal_subgroup(G, K)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2