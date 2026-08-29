import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X (represented by point stabilizer H < G)",
    "H_2: The action of G on X is primitive (H is a maximal subgroup of G)",
    "H_3: N is a non-trivial normal subgroup of G",
    "¬Q: N does not act transitively on X (G != NH)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    witness: tuple (G, H, N)
    G: PermutationGroup
    H: PermutationGroup, the point stabilizer of the action (so X = G/H)
    N: PermutationGroup, a normal subgroup of G
    """
    try:
        G, H, N = witness
        if isinstance(G, list): G = PermutationGroup(G)
        if isinstance(H, list): H = PermutationGroup(H)
        if isinstance(N, list): N = PermutationGroup(N)
    except Exception:
        return [False, False, False, False]

    def is_subgroup(A, B):
        try:
            for g in A.generators:
                if g not in B:
                    return False
            return True
        except Exception:
            return False

    def is_normal(A, B):
        try:
            if not is_subgroup(A, B):
                return False
            for b in B.generators:
                b_inv = ~b
                for a in A.generators:
                    if (b * a * b_inv) not in A:
                        return False
            return True
        except Exception:
            return False

    try:
        h1 = False
        if hasattr(G, 'generators') and hasattr(H, 'generators') and hasattr(N, 'generators'):
            if is_subgroup(H, G) and is_subgroup(N, G):
                if H.order() < G.order():
                    h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            if G.order() <= 2000:
                h2 = True
                try:
                    elements = G.elements
                except Exception:
                    elements = list(G.generate())
                for g in elements:
                    if g not in H:
                        gens = list(H.generators) + [g]
                        K = PermutationGroup(gens)
                        if K.order() < G.order():
                            h2 = False
                            break
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1:
            if N.order() > 1 and is_normal(N, G):
                h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            NH_gens = list(N.generators) + list(H.generators)
            NH = PermutationGroup(NH_gens)
            if NH.order() < G.order():
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]