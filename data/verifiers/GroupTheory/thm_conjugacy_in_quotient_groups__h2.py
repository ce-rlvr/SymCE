import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: x and y are elements of G
    try:
        h2 = bool(x in G and y in G)
    except Exception:
        h2 = False
        
    # H3: The images xN and yN are conjugate in the quotient group G/N
    try:
        h3 = False
        if getattr(G, 'is_normal', None) is not None and G.is_normal(N):
            yN = set(y * n for n in N.elements)
            for g in G.elements:
                if g * x * ~g in yN:
                    h3 = True
                    break
    except Exception:
        h3 = False
        
    # Q: There exists an element n in N such that x is conjugate to yn in G
    try:
        q = False
        if getattr(N, 'elements', None) is not None and getattr(G, 'elements', None) is not None:
            for n in N.elements:
                yn = y * n
                for h in G.elements:
                    if h * x * ~h == yn:
                        q = True
                        break
                if q:
                    break
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: The images xN and yN are conjugate in the quotient group G/N",
    "¬Q: There does not exist an element n in N such that x is conjugate to yn in G"
]

N_HYP = 3
NEG_Q_INDEX = 3