import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal_subgroup(G, H):
    """Helper to check if H is a normal subgroup of G."""
    try:
        if not isinstance(H, PermutationGroup):
            return False
        # Check if H is a subgroup of G
        for h in H.generators:
            if not G.contains(h):
                return False
        # Check normality condition: g * h * g^-1 in H for all generators
        for g in G.generators:
            g_inv = ~g
            for h in H.generators:
                if not H.contains(g * h * g_inv):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, P, p = witness
    except Exception:
        return [False] * 4 + [False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = is_normal_subgroup(G, N)
    except Exception:
        h2 = False

    # H_3: N is a nilpotent group
    try:
        if isinstance(N, PermutationGroup):
            nilp = N.is_nilpotent
            if callable(nilp):
                h3 = bool(nilp())
            else:
                h3 = bool(nilp)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: p is a prime number
    try:
        h4 = bool(isprime(p))
    except Exception:
        h4 = False

    # ¬Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal_subgroup(G, P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a nilpotent group",
    "H_4: p is a prime number",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4