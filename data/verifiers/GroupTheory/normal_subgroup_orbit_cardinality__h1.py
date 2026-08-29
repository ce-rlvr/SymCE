import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            X = witness.get('X', set(range(G.degree)))
        else:
            if len(witness) == 3:
                G, N, X = witness
            elif len(witness) == 2:
                G, N = witness
                X = set(range(G.degree))
            else:
                return [False, False, False]
        X = set(X)
    except Exception:
        return [False, False, False]

    # H_1: X is a set on which G acts transitively.
    try:
        if not X:
            h1 = False
        else:
            x0 = list(X)[0]
            # G acts transitively on X iff the orbit of any element in X is exactly X
            h1 = (set(G.orbit(x0)) == X)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G.
    try:
        if hasattr(N, 'is_normal'):
            h2 = bool(N.is_subgroup(G) and N.is_normal(G))
        else:
            h2 = bool(N.is_subgroup(G))
            if h2:
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if not N.contains(g * n * g_inv):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: Not all orbits of N on X have the same cardinality.
    try:
        if not X:
            neg_q = False
        else:
            orbits_of_N = set()
            for x in X:
                orbits_of_N.add(frozenset(N.orbit(x)))
            sizes = {len(orb) for orb in orbits_of_N}
            neg_q = len(sizes) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set on which G acts transitively",
    "H_2: N is a normal subgroup of G",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2