import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import math
import itertools
import functools

# Standard algebra objects
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
    h1 = False
    neg_q = False
    
    try:
        # The witness can be a tuple (R, f) or just the polynomial f
        if isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        else:
            R, f = None, witness

        # H_1: R is a commutative ring with identity
        if R is not None:
            if hasattr(R, 'is_commutative_ring_with_identity'):
                val = R.is_commutative_ring_with_identity
                h1 = bool(val() if callable(val) else val)
            else:
                # Assume true for standard SymPy domains or custom rings without the flag
                h1 = True  
        else:
            if hasattr(f, 'is_commutative_ring_with_identity'):
                val = f.is_commutative_ring_with_identity
                h1 = bool(val() if callable(val) else val)
            elif hasattr(f, 'domain'):
                # SymPy Poly domains are generally commutative rings with identity
                h1 = True
            else:
                h1 = False

        # ¬Q: The content ideal c(f) is the zero ideal if and only if f is the zero polynomial (must fail)
        # We check if c(f) == (0)
        if hasattr(f, 'content_ideal_is_zero'):
            val = f.content_ideal_is_zero
            c_f_is_zero = bool(val() if callable(val) else val)
        else:
            if hasattr(f, 'coeffs'):
                coeffs = f.coeffs()
            elif hasattr(f, 'as_poly') and f.as_poly() is not None:
                coeffs = f.as_poly().coeffs()
            else:
                # Fallback if we cannot extract coefficients
                coeffs = [f]
            c_f_is_zero = all(c == 0 for c in coeffs)
            
        # We check if f is the zero polynomial
        if hasattr(f, 'is_zero_polynomial'):
            val = f.is_zero_polynomial
            f_is_zero = bool(val() if callable(val) else val)
        else:
            if hasattr(f, 'is_zero'):
                f_is_zero = bool(f.is_zero)
            else:
                f_is_zero = (f == 0)
                
        # The conclusion is (c_f_is_zero == f_is_zero). We want its negation.
        neg_q = (c_f_is_zero != f_is_zero)
        
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The content ideal c(f) is the zero ideal if and only if f is the zero polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1