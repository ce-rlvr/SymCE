import sympy
import math
import itertools
import functools

class Ring:
    def __init__(self, name, noeth_domain, dim, is_field):
        self.name = name
        self.noeth_domain = noeth_domain
        self.dim = dim
        self.is_field = is_field

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
# We define a universe of standard rings and fields to be used in the witness.
ZZ = Ring("ZZ", True, 1, False)
QQ = Ring("QQ", True, 0, True)
ZZ_x = Ring("ZZ[x]", True, 2, False)
QQ_x = Ring("QQ[x]", True, 1, False)
QQ_x_frac = Ring("QQ(x)", True, 0, True)
ZZ_x_y = Ring("ZZ[x,y]", True, 3, False)
QQ_x_y = Ring("QQ[x,y]", True, 2, False)
QQ_x_y_frac = Ring("QQ(x,y)", True, 0, True)
ZZ_sqrt2 = Ring("ZZ[sqrt(2)]", True, 1, False)
QQ_sqrt2 = Ring("QQ(sqrt(2))", True, 0, True)
k_x = Ring("k[x]", True, 1, False)
k_x_frac = Ring("k(x)", True, 0, True)
k_x_y = Ring("k[x,y]", True, 2, False)
k_x_y_frac = Ring("k(x,y)", True, 0, True)

ALL_RINGS = [
    ZZ, QQ, ZZ_x, QQ_x, QQ_x_frac, ZZ_x_y, QQ_x_y, QQ_x_y_frac,
    ZZ_sqrt2, QQ_sqrt2, k_x, k_x_frac, k_x_y, k_x_y_frac
]

# Directed edges representing immediate subring relationships
_subring_edges = [
    (ZZ, QQ),
    (ZZ, ZZ_x),
    (ZZ, ZZ_sqrt2),
    (ZZ_sqrt2, QQ_sqrt2),
    (QQ, QQ_sqrt2),
    (QQ, QQ_x),
    (ZZ_x, QQ_x),
    (ZZ_x, ZZ_x_y),
    (QQ_x, QQ_x_frac),
    (QQ_x, QQ_x_y),
    (ZZ_x_y, QQ_x_y),
    (QQ_x_y, QQ_x_y_frac),
    (QQ_x_frac, QQ_x_y_frac),
    (k_x, k_x_frac),
    (k_x, k_x_y),
    (k_x_y, k_x_y_frac),
    (k_x_frac, k_x_y_frac)
]

def is_subring(A, B):
    if A == B:
        return True
    adj = {r: set() for r in ALL_RINGS}
    for u, v in _subring_edges:
        adj[u].add(v)
    
    visited = set([A])
    queue = [A]
    while queue:
        curr = queue.pop(0)
        if curr == B:
            return True
        for nxt in adj[curr]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return False

def is_finite_ext(L, K):
    if not (getattr(L, 'is_field', False) and getattr(K, 'is_field', False)):
        return False
    if L == K:
        return True
    finite_exts = [
        (QQ, QQ_sqrt2)
    ]
    return (K, L) in finite_exts

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            K = witness.get("K")
            L = witness.get("L")
            S = witness.get("S")
        elif hasattr(witness, "R"):
            R = witness.R
            K = witness.K
            L = witness.L
            S = witness.S
        else:
            R, K, L, S = witness
    except Exception:
        return [False] * 5

    # H1: R is a commutative Noetherian integral domain
    try:
        h1 = bool(R.noeth_domain)
    except Exception:
        h1 = False

    # H2: The Krull dimension of R is 1
    try:
        h2 = bool(R.dim == 1)
    except Exception:
        h2 = False

    # H3: L is a finite algebraic field extension of K
    try:
        h3 = bool(is_finite_ext(L, K))
    except Exception:
        h3 = False

    # H4: S is a subring of L such that R \subseteq S \subseteq L
    try:
        h4 = bool(is_subring(R, S) and is_subring(S, L))
    except Exception:
        h4 = False

    # neg_Q: S is NOT a one-dimensional Noetherian ring
    try:
        neg_q = not (S.noeth_domain and S.dim == 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: The Krull dimension of R is 1",
    "H_3: L is a finite algebraic field extension of K",
    "H_4: S is a subring of L such that R \\subseteq S \\subseteq L",
    "¬Q: S is not a one-dimensional Noetherian ring"
]

N_HYP = 4
NEG_Q_INDEX = 4