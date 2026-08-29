import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract G, N, and optionally X from the witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                X = list(range(max(getattr(G, 'degree', 0), getattr(N, 'degree', 0))))
            elif len(witness) >= 3:
                G, N, X = witness[:3]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if h1 and isinstance(N, PermutationGroup):
            # Check if N is a subgroup of G
            is_sub = all(G.contains(gen) for gen in N.generators)
            if is_sub:
                # Check normality: g * n * g^-1 in N for all generators
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        conj = g * n * g_inv
                        if not N.contains(conj):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # neg_Q: All orbits of N on X do NOT have the same cardinality
    try:
        neg_q = False
        if isinstance(N, PermutationGroup) and hasattr(X, '__iter__'):
            X_list = list(X)
            X_set = set(X_list)
            visited = set()
            sizes = set()
            for x in X_list:
                if x not in visited:
                    orbit = set([x])
                    queue = [x]
                    while queue:
                        curr = queue.pop(0)
                        for n in N.generators:
                            next_pt = curr
                            # Apply permutation if the point is within its domain
                            if isinstance(curr, int) and curr >= 0 and curr < n.size:
                                next_pt = n.array_form[curr]
                            if next_pt in X_set and next_pt not in orbit:
                                orbit.add(next_pt)
                                queue.append(next_pt)
                    visited.update(orbit)
                    sizes.add(len(orbit))
            # The conclusion fails if there are orbits of different sizes
            neg_q = len(sizes) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: All orbits of N on X do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2