import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
        G, N, X, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        h1 = False
        # Check if N is a subgroup of G
        if all(n in G for n in N.generators):
            h1 = True
            # Check normality: g * n * g^-1 in N for all g in G, n in N
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: N acts transitively on X
    try:
        h2 = False
        if X:
            X_set = set(X)
            invariant = True
            # Check if X is invariant under N
            for n in N.generators:
                for a in X_set:
                    if n(a) not in X_set:
                        invariant = False
                        break
                if not invariant:
                    break
            
            # Check if the orbit of an element equals X
            if invariant:
                a = next(iter(X_set))
                orbit = set(N.orbit(a))
                if orbit == X_set:
                    h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # neg_Q: G != N G_x
    try:
        neg_q = False
        G_x = G.stabilizer(x)
        N_elems = list(N.generate())
        Gx_elems = list(G_x.generate())
        
        # Compute the set of elements in N * G_x
        NGx = set(n * h for n in N_elems for h in Gx_elems)
        
        # Get the order of G safely
        try:
            g_order = G.order()
        except TypeError:
            g_order = G.order
        except AttributeError:
            g_order = len(list(G.generate()))
            
        # Since N * G_x is a subset of G, they are equal iff their sizes are equal
        if g_order != len(NGx):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: G != N G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3