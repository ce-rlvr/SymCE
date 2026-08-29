import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (G, f) where G is a group and f is a map G -> G.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, f = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = False
        if hasattr(G, "elements") and hasattr(G, "is_abelian"):
            elements = list(G.elements)
            if len(elements) > 0:
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion "f is a group homomorphism iff G is an abelian group" FAILS
    try:
        if not h1:
            neg_q = False
        else:
            is_abelian = bool(G.is_abelian)
            
            is_hom = True
            for x in elements:
                for y in elements:
                    xy = x * y
                    
                    if callable(f):
                        f_x = f(x)
                        f_y = f(y)
                        f_xy = f(xy)
                    else:
                        f_x = f[x]
                        f_y = f[y]
                        f_xy = f[xy]
                        
                    if f_xy != f_x * f_y:
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
            # The conclusion is (is_hom == is_abelian). We want its negation.
            neg_q = (is_hom != is_abelian)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The equivalence (f is a group homomorphism iff G is an abelian group) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1