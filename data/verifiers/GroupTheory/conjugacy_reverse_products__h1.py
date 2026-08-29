import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
import itertools
import math
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

def in_G(elem, G):
    try:
        if elem in G:
            return True
    except Exception:
        pass
    try:
        if G.contains(elem):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, x, y) where G is a set/list/monoid,
    and x, y are elements of G.
    """
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: Let x and y be elements of G
        h1 = in_G(x, G) and in_G(y, G)
    except Exception:
        h1 = False
        
    try:
        # ¬Q: The product xy is NOT conjugate to the product yx in G
        # Conjugacy in G means there exists an invertible element g in G 
        # (with its inverse also in G) such that g * yx * g^-1 == xy
        xy = x * y
        yx = y * x
        
        conjugate = False
        for g in G:
            try:
                # Attempt to find the inverse of g
                if hasattr(g, 'inv'):
                    ginv = g.inv()
                else:
                    try:
                        ginv = ~g
                    except Exception:
                        ginv = g**-1
                
                # The inverse must also be in G for the conjugacy to be "in G"
                if not in_G(ginv, G):
                    continue
                
                # Check if g conjugates yx to xy
                if g * yx * ginv == xy:
                    conjugate = True
                    break
            except Exception:
                # If g is not invertible or multiplication fails, just continue
                pass
                
        neg_q = not conjugate
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let x and y be elements of G",
    "¬Q: The product xy is not conjugate to the product yx in G"
]

N_HYP = 1
NEG_Q_INDEX = 1