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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            G = witness[0]
            N = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: G is a primitive permutation group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and G.is_primitive()
    except Exception:
        h1 = False

    # ¬Q: The action of N on X is not transitive
    try:
        if not isinstance(N, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            # N is transitive on X (the domain of G) iff it is transitive and has the same degree as G.
            # If N.degree < G.degree, N fixes some points in X and thus is not transitive on X 
            # (unless G.degree == 1, in which case N.degree is also 1).
            is_transitive_on_X = N.is_transitive() and (N.degree == G.degree)
            neg_q = not is_transitive_on_X
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a primitive permutation group acting on a set X",
    "¬Q: The action of N on X is not transitive"
]

N_HYP = 1
NEG_Q_INDEX = 1