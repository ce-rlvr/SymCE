import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import isprime

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

def _is_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    try:
        for g in H.generators:
            if not G.contains(g):
                return False
        return True
    except Exception:
        return False

def _is_normal(H, G):
    if not _is_subgroup(H, G):
        return False
    try:
        for g in G.generators:
            g_inv = ~g
            for h in H.generators:
                conj = g * h * g_inv
                if not H.contains(conj):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        N = witness.get('N')
        P = witness.get('P')
        p = witness.get('p')
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        G, N, P, p = witness
    else:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = _is_normal(N, G)
    except Exception:
        h3 = False

    # neg_Q: P is not a normal subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            neg_q = False
        else:
            neg_q = not _is_normal(P, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is a normal subgroup of G",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3