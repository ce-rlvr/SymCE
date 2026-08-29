import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            if G is None or N is None:
                return [False, False, False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, N = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and N.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: X is a set
    try:
        # In our representation, X is the set {0, 1, ..., G.degree - 1}
        h2 = h1
    except Exception:
        h2 = False

    # H_3: G acts transitively on X
    try:
        if h1:
            if callable(G.is_transitive):
                h3 = bool(G.is_transitive())
            else:
                h3 = bool(G.is_transitive)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: Not all orbits of N on X have the same cardinality
    try:
        if not h1:
            neg_q = False
        else:
            degree = G.degree
            if degree == 0:
                neg_q = False
            else:
                visited = set()
                orbit_sizes = []
                for i in range(degree):
                    if i not in visited:
                        orbit = {i}
                        queue = [i]
                        while queue:
                            curr = queue.pop(0)
                            for g in N.generators:
                                nxt = g(curr)
                                if nxt not in orbit:
                                    orbit.add(nxt)
                                    queue.append(nxt)
                        visited.update(orbit)
                        orbit_sizes.append(len(orbit))
                neg_q = len(set(orbit_sizes)) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3