import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, p = witness
            elif len(witness) == 2:
                G, N = witness
                p = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: Let G be a finite group
    try:
        h1 = hasattr(G, 'order') and hasattr(G, 'generators')
        if h1:
            order = G.order()
            h1 = (order > 0) and (order != float('inf'))
    except Exception:
        h1 = False

    # H_2: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    try:
        h2 = False
        if h1:
            h2 = True
            for H in G.normal_subgroups():
                if H.order() > 1 and H.is_abelian:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: Let N be a normal subgroup of G
    try:
        h3 = False
        if h1 and hasattr(N, 'generators') and hasattr(N, 'order'):
            h3 = True
            # Check if N is a subgroup of G
            for gen in N.generators:
                if gen not in G:
                    h3 = False
                    break
            # Check if N is normal in G
            if h3:
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            h3 = False
                            break
    except Exception:
        h3 = False

    # ¬Q: The order of the subgroup N is equal to p
    try:
        if p is not None:
            neg_q = (N.order() == p)
        else:
            from sympy.ntheory import isprime
            neg_q = isprime(N.order())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: N is a normal subgroup of G",
    "¬Q: The order of the subgroup N is equal to p"
]

N_HYP = 3
NEG_Q_INDEX = 3