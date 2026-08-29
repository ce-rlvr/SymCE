import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if h1 and isinstance(N, PermutationGroup):
            # Check if N is a subgroup of G
            is_sub = all(gen in G for gen in N.generators)
            
            # Check normality: g * n * g^-1 in N for all generators
            is_normal = True
            if is_sub:
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            h2 = is_sub and is_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: G/N is solvable
    # G/N is solvable iff the derived series of G eventually lands inside N
    try:
        if h1 and h2:
            curr = G
            while True:
                next_G = curr.derived_subgroup()
                curr_order = curr.order() if callable(getattr(curr, 'order', None)) else curr.order
                next_order = next_G.order() if callable(getattr(next_G, 'order', None)) else next_G.order
                if next_order == curr_order:
                    break
                curr = next_G
            h3 = all(gen in N for gen in curr.generators)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is not solvable
    try:
        if h1:
            solvable = G.is_solvable
            if callable(solvable):
                solvable = solvable()
            neg_q = not solvable
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G/N is solvable",
    "¬Q: G is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3