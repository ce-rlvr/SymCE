import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) < 2:
            return [False, False, False]
        G, N = witness[0], witness[1]
    except Exception:
        return [False, False, False]
    
    # H1: G is a group and N is a subgroup of G
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1_ok:
            for g in N.generators:
                if not G.contains(g):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H2: G acts transitively on X
    try:
        transitive = G.is_transitive() if callable(G.is_transitive) else G.is_transitive
        h2_ok = bool(transitive)
    except Exception:
        h2_ok = False

    # Neg_Q: Not all orbits of N on X have the same cardinality
    try:
        if N.degree > G.degree:
            neg_q_ok = False
        else:
            orbits = N.orbits() if callable(N.orbits) else N.orbits
            orbit_sizes = [len(o) for o in orbits]
            # Points from N.degree to G.degree - 1 are fixed by N, forming orbits of size 1
            orbit_sizes += [1] * (G.degree - N.degree)
            neg_q_ok = len(set(orbit_sizes)) > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: X is a set on which G acts transitively",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2