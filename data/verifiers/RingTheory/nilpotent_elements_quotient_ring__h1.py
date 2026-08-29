import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (R, I, x).
    """
    try:
        R, I, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: I is an ideal of R
    h1 = False
    try:
        if hasattr(I, 'is_ideal'):
            h1 = I.is_ideal(R)
        elif hasattr(I, 'ring'):
            h1 = (I.ring == R)
        elif isinstance(I, list) and isinstance(R, list):
            h1 = all(elem in R for elem in I)
        elif hasattr(witness, 'is_ideal'):
            h1 = witness.is_ideal()
    except Exception:
        pass
        
    # H_2: x is an element of R
    h2 = False
    try:
        if hasattr(R, '__contains__'):
            h2 = (x in R)
        elif hasattr(x, 'ring'):
            h2 = (x.ring == R)
        elif isinstance(R, list):
            h2 = (x in R)
        elif hasattr(witness, 'is_element'):
            h2 = witness.is_element()
    except Exception:
        pass
        
    # ¬Q: The coset x + I is a nilpotent element in the quotient ring R/I 
    # if and only if there exists a positive integer n such that x^n \in I (must FAIL)
    neg_q = False
    try:
        # Check if there exists n > 0 such that x^n \in I
        xn_in_I = False
        xn = x
        for n in range(1, 100):
            in_I = False
            if hasattr(I, '__contains__'):
                in_I = (xn in I)
            elif hasattr(I, 'contains'):
                in_I = I.contains(xn)
            elif isinstance(I, list):
                in_I = (xn in I)
                
            if in_I:
                xn_in_I = True
                break
            xn = xn * x
            
        # Check if x + I is nilpotent in R/I
        coset_nilpotent = False
        if hasattr(R, 'quotient_ring'):
            Q = R.quotient_ring(I)
            x_bar = Q(x)
            xn_bar = x_bar
            for n in range(1, 100):
                if xn_bar == Q.zero:
                    coset_nilpotent = True
                    break
                xn_bar = xn_bar * x_bar
        elif hasattr(witness, 'is_coset_nilpotent'):
            coset_nilpotent = witness.is_coset_nilpotent()
        else:
            # Fallback if quotient ring cannot be explicitly constructed
            coset_nilpotent = xn_in_I
            
        # The conclusion fails if the two conditions are not equivalent
        neg_q = (coset_nilpotent != xn_in_I)
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x is an element of R",
    "¬Q: x + I is nilpotent in R/I is NOT equivalent to exists n > 0 such that x^n in I"
]

N_HYP = 2
NEG_Q_INDEX = 2