import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, N = witness
            Phi_given = False
        elif len(witness) == 3:
            G, N, Phi = witness
            Phi_given = True
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def apply_map(F, x):
        if callable(F):
            return F(x)
        return F[x]

    def inverse(g):
        try:
            return g**-1
        except Exception:
            return ~g

    try:
        G_elements = list(G.elements)
        N_elements = list(N.elements)
    except Exception:
        return [False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal') and hasattr(N, 'is_subgroup'):
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
        else:
            is_sub = all(n in G_elements for n in N_elements)
            is_norm = True
            if is_sub:
                for g in G_elements:
                    for n in N_elements:
                        if (g * n * inverse(g)) not in N_elements:
                            is_norm = False
                            break
                    if not is_norm:
                        break
            h1 = is_sub and is_norm
    except Exception:
        h1 = False

    # H_2: \Phi is the homomorphism defined by \Phi(g)(n) = gng^{-1}
    try:
        if Phi_given:
            h2 = True
            for g in G_elements:
                for n in N_elements:
                    if apply_map(apply_map(Phi, g), n) != g * n * inverse(g):
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The kernel of \Phi is not the centralizer C_G(N)
    try:
        kernel = []
        if Phi_given:
            for g in G_elements:
                if all(apply_map(apply_map(Phi, g), n) == n for n in N_elements):
                    kernel.append(g)
        else:
            for g in G_elements:
                if all(g * n * inverse(g) == n for n in N_elements):
                    kernel.append(g)

        centralizer = []
        for g in G_elements:
            if all(g * n == n * g for n in N_elements):
                centralizer.append(g)

        def is_equal_sets(list1, list2):
            for x in list1:
                if x not in list2:
                    return False
            for x in list2:
                if x not in list1:
                    return False
            return True

        neg_q = not is_equal_sets(kernel, centralizer)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: Phi is the homomorphism defined by conjugation",
    "¬Q: The kernel of Phi is not the centralizer C_G(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2