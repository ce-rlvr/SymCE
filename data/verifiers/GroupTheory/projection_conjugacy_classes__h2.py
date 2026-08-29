import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, x, y).
    """
    try:
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'generators')
    except Exception:
        h1 = False
        
    # H_2: x and y are elements of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(x) and G.contains(y))
        else:
            h2 = bool(x in G.elements and y in G.elements)
    except Exception:
        h2 = False
        
    # H_3: x and y are conjugate in G
    try:
        h3 = False
        if h2:
            for g in G.elements:
                if g * x * g**-1 == y:
                    h3 = True
                    break
    except Exception:
        h3 = False
        
    # neg_Q: The images xN and yN are conjugate in the quotient group G/N
    # If N is a normal subgroup of G, G/N is a quotient group and xN, yN are guaranteed to be conjugate.
    # The conclusion fails if G/N is not a valid quotient group (i.e., N is not a normal subgroup).
    try:
        if hasattr(N, 'is_normal') and hasattr(N, 'is_subgroup'):
            is_normal = N.is_subgroup(G) and N.is_normal(G)
            neg_q = not is_normal
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: x and y are conjugate in G",
    "¬Q: The images xN and yN are not conjugate in the quotient group G/N (e.g., G/N is not a group)"
]

N_HYP = 3
NEG_Q_INDEX = 3