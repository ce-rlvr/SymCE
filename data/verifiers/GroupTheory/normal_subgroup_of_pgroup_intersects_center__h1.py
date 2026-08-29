import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
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

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is not the trivial subgroup",
    "¬Q: The intersection of N and Z(G) is the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite p-group
    try:
        order = G.order()
        factors = sympy.ntheory.factorint(order)
        # A non-trivial finite p-group has exactly one prime factor in its order.
        # (If G is trivial, N would be trivial, failing H_3 anyway).
        h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        # Check if N is a subgroup of G
        is_sub = all(G.contains(h) for h in N.generators)
        is_norm = is_sub
        # Check if N is normal in G
        if is_norm:
            for g in G.generators:
                for h in N.generators:
                    if not N.contains(g * h * ~g):
                        is_norm = False
                        break
                    if not N.contains(~g * h * g):
                        is_norm = False
                        break
                if not is_norm:
                    break
        h2 = is_norm
    except Exception:
        h2 = False

    # H_3: N is not the trivial subgroup
    try:
        h3 = N.order() > 1
    except Exception:
        h3 = False

    # ¬Q: The intersection of N and Z(G) is the trivial subgroup
    try:
        Z = G.center()
        neg_q = True
        # If there is any non-identity element in both N and Z(G), the intersection is non-trivial.
        for n in N.elements:
            if not n.is_Identity and Z.contains(n):
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]