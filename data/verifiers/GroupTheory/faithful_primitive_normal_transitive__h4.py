import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a tuple (G, N) where G is a permutation group
    and N is a normal subgroup of G.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X and N is a normal subgroup of G
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            if N.is_subgroup(G):
                is_normal = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if (g * n * g_inv) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h1 = is_normal
    except Exception:
        h1 = False

    # H_2: The action of G on X is faithful
    try:
        # In SymPy, a PermutationGroup acts faithfully on its domain by definition.
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: The action of G on X is primitive
    try:
        h3 = bool(G.is_primitive())
    except Exception:
        h3 = False

    # ¬Q: The normal subgroup N does not act transitively on X
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and G.degree > 0:
            # N acts transitively on X (the domain of G) iff the orbit of 0 under N has size G.degree
            neg_q = len(N.orbit(0)) != G.degree
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X and N is a normal subgroup of G",
    "H_2: The action of G on X is faithful",
    "H_3: The action of G on X is primitive",
    "¬Q: The normal subgroup N does not act transitively on X"
]

N_HYP = 3
NEG_Q_INDEX = 3