import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    def is_normal_subgroup(N, Grp):
        try:
            if not N.is_subgroup(Grp):
                return False
            for g in Grp.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        return False
            return True
        except Exception:
            return False

    # H_1: G is a group and K is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: H is a normal subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and is_normal_subgroup(H, G)
    except Exception:
        h2 = False

    # neg_Q: The mutual commutator subgroup of H and K is not a normal subgroup of G
    try:
        commutators = []
        for h in list(H.elements):
            for k in list(K.elements):
                commutators.append(h * k * ~h * ~k)
        HK_comm = PermutationGroup(commutators)
        
        neg_q = not is_normal_subgroup(HK_comm, G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and K is a subgroup of G",
    "H_2: H is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2