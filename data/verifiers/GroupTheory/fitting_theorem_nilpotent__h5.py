import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

def is_normal_subgroup(G, H):
    """Helper to check if H is a normal subgroup of G."""
    try:
        if not isinstance(H, PermutationGroup):
            return False
        # Check if H is a subgroup of G
        for h in H.generators:
            if not G.contains(h):
                return False
        # Check normality: g * h * g^-1 in H for all generators
        for g in G.generators:
            for h in H.generators:
                if not H.contains(g * h * ~g):
                    return False
                if not H.contains(~g * h * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False] * 5
        G, M, N = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: M is a normal subgroup of G
    try:
        h2 = is_normal_subgroup(G, M)
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = is_normal_subgroup(G, N)
    except Exception:
        h3 = False

    # H_4: M is a nilpotent group
    try:
        h4 = bool(M.is_nilpotent)
    except Exception:
        h4 = False

    # ¬Q: The product MN is not a normal nilpotent subgroup of G
    try:
        MN_gens = list(M.generators) + list(N.generators)
        if not MN_gens:
            MN_gens = [G.generators[0]**0] if getattr(G, 'generators', None) else [Permutation(0)]
        MN = PermutationGroup(MN_gens)
        
        is_normal = is_normal_subgroup(G, MN)
        is_nilp = bool(MN.is_nilpotent)
        
        # The conclusion is that MN is a normal nilpotent subgroup.
        # We want the negation of this conclusion.
        neg_q = not (is_normal and is_nilp)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: N is a normal subgroup of G",
    "H_4: M is a nilpotent group",
    "¬Q: The product MN is not a normal nilpotent subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4