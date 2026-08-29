import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, A, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: A is an abelian normal subgroup of G
    try:
        if not A.is_subgroup(G):
            h1 = False
        elif not A.is_abelian:
            h1 = False
        else:
            # Check normality manually to be safe
            is_normal = True
            for g in G.generators:
                g_inv = ~g
                for a in A.generators:
                    if (g * a * g_inv) not in A:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h1 = is_normal
    except Exception:
        h1 = False
        
    # H_2: x is an element of G
    try:
        h2 = bool(x in G)
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x in G does NOT divide the index of A in G
    try:
        # Compute the conjugacy class of x in G
        orbit = {x}
        queue = [x]
        gens = G.generators
        for elem in queue:
            for g in gens:
                conj = g * elem * ~g
                if conj not in orbit:
                    orbit.add(conj)
                    queue.append(conj)
        
        c_size = len(orbit)
        index = G.order() // A.order()
        
        # The conclusion fails if the conjugacy class size does not divide the index
        neg_q = bool(index % c_size != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian normal subgroup of G",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2