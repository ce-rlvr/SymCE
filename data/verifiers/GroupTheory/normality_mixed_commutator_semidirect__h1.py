import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def is_subgroup(sub, grp):
    for gen in sub.generators:
        if not grp.contains(gen):
            return False
    return True

def is_normal_subgroup(sub, grp):
    if not is_subgroup(sub, grp):
        return False
    for g in grp.generators:
        for h in sub.generators:
            if not sub.contains(g * h * (~g)):
                return False
            if not sub.contains((~g) * h * g):
                return False
    return True

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        h1 = bool(is_normal_subgroup(N, G))
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = bool(is_subgroup(H, G))
    except Exception:
        h2 = False

    # H3: G is the internal semidirect product of N and H
    try:
        if not (h1 and h2):
            h3 = False
        else:
            n_elements = set(N.generate_dimino())
            h_elements = set(H.generate_dimino())
            intersection = n_elements.intersection(h_elements)
            if len(intersection) != 1:
                h3 = False
            elif N.order() * H.order() != G.order():
                h3 = False
            else:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: The mixed commutator subgroup is NOT a normal subgroup of G
    try:
        commutators = set()
        for n in N.generate_dimino():
            for h in H.generate_dimino():
                comm = n * h * (~n) * (~h)
                commutators.add(comm)
        K = PermutationGroup(list(commutators))
        neg_q = not is_normal_subgroup(K, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: The mixed commutator subgroup is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3