import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            X = witness.get('X', list(range(G.degree)))
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, X, N = witness
            elif len(witness) == 2:
                G, N = witness
                X = list(range(G.degree))
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: X is a set
    try:
        h1 = isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H_2: G acts transitively on X
    try:
        if not h1:
            h2 = False
        else:
            X_set = set(X)
            if len(X_set) == 0:
                h2 = True
            else:
                invariant = True
                for x in X_set:
                    for g in G.generators:
                        if g(x) not in X_set:
                            invariant = False
                            break
                    if not invariant:
                        break
                if not invariant:
                    h2 = False
                else:
                    x0 = next(iter(X_set))
                    orbit_x0 = set(G.orbit(x0))
                    h2 = (orbit_x0 == X_set)
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        is_subgroup = all(G.contains(g) for g in N.generators)
        is_normal = True
        if is_subgroup:
            for n in N.generators:
                for g in G.generators:
                    if not N.contains(g * n * ~g) or not N.contains(~g * n * g):
                        is_normal = False
                        break
                if not is_normal:
                    break
        h3 = is_subgroup and is_normal
    except Exception:
        h3 = False

    # ¬Q: Not all orbits of N on X have the same cardinality
    try:
        if not h1:
            neg_q = False
        else:
            X_set = set(X)
            if len(X_set) == 0:
                neg_q = False
            else:
                unvisited = set(X_set)
                orbit_sizes = set()
                while unvisited:
                    x = unvisited.pop()
                    orb = set(N.orbit(x)).intersection(X_set)
                    orbit_sizes.add(len(orb))
                    unvisited -= orb
                neg_q = len(orbit_sizes) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts transitively on X",
    "H_3: N is a normal subgroup of G",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3