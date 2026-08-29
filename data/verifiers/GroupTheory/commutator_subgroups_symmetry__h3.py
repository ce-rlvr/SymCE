import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_commutator_subgroup(H, K):
    if hasattr(H, 'commutator'):
        try:
            return H.commutator(K)
        except Exception:
            pass
    gens = []
    for h in list(H.generate()):
        for k in list(K.generate()):
            gens.append(h * k * (~h) * (~k))
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            K = witness.get('K')
        else:
            G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: The commutator subgroup of H and K is not equal to that of K and H
    try:
        if not isinstance(K, PermutationGroup):
            neg_q = False
        else:
            HK = get_commutator_subgroup(H, K)
            KH = get_commutator_subgroup(K, H)
            neg_q = bool(HK != KH)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "not Q: The commutator subgroup of H and K is not equal to that of K and H"
]

N_HYP = 2
NEG_Q_INDEX = 2