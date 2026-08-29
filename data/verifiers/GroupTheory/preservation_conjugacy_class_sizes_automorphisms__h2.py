import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, x, phi = witness
        elif len(witness) == 2:
            G, x = witness
            phi = x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        h2 = bool(G.contains(x))
    except Exception:
        h2 = False

    # neg_Q: The cardinality of the conjugacy class of x in G is not equal to the cardinality of the conjugacy class of phi(x) in G
    try:
        if isinstance(phi, dict):
            phix = phi[x]
        elif hasattr(phi, '__call__'):
            try:
                phix = phi(x)
            except Exception:
                phix = phi
        else:
            phix = phi
            
        if not G.contains(phix):
            neg_q = False
        else:
            try:
                # Fast path using Orbit-Stabilizer theorem
                cx_size = G.order() // G.centralizer(x).order()
                cphix_size = G.order() // G.centralizer(phix).order()
                neg_q = bool(cx_size != cphix_size)
            except Exception:
                # Fallback to naive computation
                if G.order() > 5000:
                    neg_q = False
                else:
                    orbit_x = set()
                    orbit_phix = set()
                    for g in G.elements:
                        orbit_x.add(g * x * ~g)
                        orbit_phix.add(g * phix * ~g)
                    neg_q = len(orbit_x) != len(orbit_phix)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The cardinality of the conjugacy class of x in G is not equal to the cardinality of the conjugacy class of phi(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2