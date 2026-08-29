import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
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
        G = witness
        
        # Compute the center of the group
        Z = G.center()
        Z_elements = set(Z.elements)
        
        # Compute the intersection of the centralizers of all elements
        elements = list(G.elements)
        C_int_elements = set(elements)
        for x in elements:
            C_x = G.centralizer(x)
            C_int_elements = C_int_elements.intersection(set(C_x.elements))
            
        # The conclusion is that Z(G) == intersection of C_G(x).
        # We want neg_Q to be True if the conclusion FAILS.
        neg_Q = bool(Z_elements != C_int_elements)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The center Z(G) is not equal to the intersection over all elements x in G of the centralizer C_G(x)"
]

N_HYP = 0
NEG_Q_INDEX = 0