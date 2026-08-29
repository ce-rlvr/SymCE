import sympy
from sympy import *
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    The conjecture is:
    Hypotheses:
      - R is a commutative ring
      - I is an ideal of R
    Conclusion:
      Tor_1^R(R/I, R/J) is isomorphic to (I \cap J)/IJ
      
    This theorem is unconditionally true if J is also an ideal of R.
    The dropped hypothesis is "J is an ideal of R".
    Therefore, the conclusion fails (is mathematically ill-typed/undefined) 
    exactly when J is NOT an ideal of R.
    
    Expected witness: a tuple (R, I, J)
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            # Fallback: assume true if it's a valid object and doesn't explicitly deny commutativity
            h1 = True
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        if isinstance(I, (list, tuple, set)):
            # A list of generators defines an ideal
            h2 = True
        elif hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal(R))
        else:
            # If I is a subring (contains 1) and I != R, it is not an ideal.
            is_ring = False
            if hasattr(I, 'is_Ring') and I.is_Ring:
                is_ring = True
            elif hasattr(I, 'is_commutative'):
                is_ring = True
            elif I in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
                is_ring = True
            elif hasattr(I, 'get_ring') or hasattr(I, 'of_type'):
                is_ring = True
                
            if is_ring and I != R:
                h2 = False
            else:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails (J is not an ideal)
    try:
        is_J_ideal = True
        if isinstance(J, (list, tuple, set)):
            is_J_ideal = True
        elif hasattr(J, 'is_ideal'):
            is_J_ideal = bool(J.is_ideal(R))
        else:
            # If J is a subring (contains 1) and J != R, it is not an ideal.
            is_ring = False
            if hasattr(J, 'is_Ring') and J.is_Ring:
                is_ring = True
            elif hasattr(J, 'is_commutative'):
                is_ring = True
            elif J in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
                is_ring = True
            elif hasattr(J, 'get_ring') or hasattr(J, 'of_type'):
                is_ring = True
                
            if is_ring and J != R:
                is_J_ideal = False
                
        neg_q = not is_J_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "not Q: Tor_1^R(R/I, R/J) is not isomorphic to (I \\cap J)/IJ (fails because J is not an ideal)"
]

N_HYP = 2
NEG_Q_INDEX = 2