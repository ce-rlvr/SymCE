import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

def is_subgroup(K, G):
    if not hasattr(K, 'generators') or not hasattr(G, 'generators'):
        return False
    for k in K.generators:
        if not G.contains(k):
            return False
    return True

def is_normal(K, G):
    if not is_subgroup(K, G):
        return False
    for g in G.generators:
        for k in K.generators:
            if not K.contains((~g) * k * g):
                return False
            if not K.contains(g * k * (~g)):
                return False
    return True

def mutual_commutator(H, K):
    gens = []
    H_elems = list(H.elements) if hasattr(H, 'elements') else list(H.generate())
    K_elems = list(K.elements) if hasattr(K, 'elements') else list(K.generate())
    for h in H_elems:
        for k in K_elems:
            gens.append((~h) * (~k) * h * k)
    if not gens:
        gens = [Permutation(0)]
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = hasattr(G, 'generators') and is_subgroup(H, G) and is_subgroup(K, G)
    except Exception:
        h1 = False

    try:
        h2 = is_normal(K, G)
    except Exception:
        h2 = False

    try:
        HK_comm = mutual_commutator(H, K)
        neg_q = not is_normal(HK_comm, G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2