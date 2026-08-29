import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def commutator_subgroup(A, B):
    gens = set()
    A_elems = list(A.generate())
    B_elems = list(B.generate())
    if len(A_elems) > 500 or len(B_elems) > 500:
        raise ValueError("Groups too large")
    for a in A_elems:
        for b in B_elems:
            gens.add(~a * ~b * a * b)
    if not gens:
        return PermutationGroup([Permutation()])
    return PermutationGroup(list(gens))

def conditions(witness) -> list[bool]:
    try:
        G, X, Y, Z = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(X, PermutationGroup) and 
              isinstance(Y, PermutationGroup) and 
              isinstance(Z, PermutationGroup) and 
              all(g in G for g in X.generators) and 
              all(g in G for g in Y.generators) and 
              all(g in G for g in Z.generators))
    except Exception:
        h2 = False

    try:
        YZ = commutator_subgroup(Y, Z)
        YZ_X = commutator_subgroup(YZ, X)
        h3 = all(g.is_Identity for g in YZ_X.generators)
    except Exception:
        h3 = False

    try:
        ZX = commutator_subgroup(Z, X)
        ZX_Y = commutator_subgroup(ZX, Y)
        neg_q = not all(g.is_Identity for g in ZX_Y.generators)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X, Y, and Z are subgroups of G",
    "H_3: commutator(commutator(Y, Z), X) is the trivial subgroup",
    "¬Q: commutator(commutator(Z, X), Y) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3