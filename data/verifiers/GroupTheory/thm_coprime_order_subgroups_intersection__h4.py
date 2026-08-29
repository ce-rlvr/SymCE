import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings for witness expressions
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a finite subgroup of G
    try:
        h2 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(G.contains(g) for g in H.generators)
    except Exception:
        h2 = False

    # H_3: K is a finite subgroup of G
    try:
        h3 = False
        if isinstance(K, PermutationGroup) and isinstance(G, PermutationGroup):
            h3 = all(G.contains(g) for g in K.generators)
    except Exception:
        h3 = False

    # neg_Q: The intersection H \cap K is not the trivial subgroup {e}
    try:
        neg_q = False
        if isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            identity = H.identity
            for g in H.generate():
                if g != identity:
                    try:
                        if K.contains(g):
                            neg_q = True
                            break
                    except Exception:
                        pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a finite subgroup of G",
    "H_3: K is a finite subgroup of G",
    "¬Q: The intersection H \\cap K is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3