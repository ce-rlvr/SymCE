import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: n is a non-negative integer
    try:
        h2 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0
    except Exception:
        h2 = False

    # ¬Q: The n-th derived subgroup H^(n) is NOT a subgroup of the n-th derived subgroup G^(n)
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            # Compute G^(n)
            G_n = G
            for _ in range(n):
                next_G = G_n.derived_subgroup()
                if next_G.order() == G_n.order():
                    break
                G_n = next_G
                
            # Compute H^(n)
            H_n = H
            for _ in range(n):
                next_H = H_n.derived_subgroup()
                if next_H.order() == H_n.order():
                    break
                H_n = next_H
                
            # Check if H_n is a subgroup of G_n
            is_subgroup = True
            for g in H_n.generators:
                if g.is_Identity:
                    continue
                try:
                    # Adjust permutation degree to match G_n for safe membership testing
                    if g.size < G_n.degree:
                        new_array = g.array_form + list(range(g.size, G_n.degree))
                        g_check = Permutation(new_array)
                    elif g.size > G_n.degree:
                        # If g moves any element outside G_n's domain, it cannot be in G_n
                        if any(i != g.array_form[i] for i in range(G_n.degree, g.size)):
                            is_subgroup = False
                            break
                        g_check = Permutation(g.array_form[:G_n.degree])
                    else:
                        g_check = g
                        
                    if g_check not in G_n:
                        is_subgroup = False
                        break
                except Exception:
                    is_subgroup = False
                    break
                    
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a non-negative integer",
    "¬Q: H^(n) is not a subgroup of G^(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2