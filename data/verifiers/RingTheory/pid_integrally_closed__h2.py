import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import math
import itertools
import functools

from sympy import ZZ, QQ, Symbol, minpoly, I, sqrt, Rational
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: R is not integrally closed in K"
]

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    
    The witness is expected to be a tuple (R, K) where R is a ring (e.g., ZZ)
    and K is an extension ring/field or a generator of the extension (e.g., sqrt(5)).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, K = witness
        else:
            R = witness
            K = None
    except Exception:
        return [False, False]
    
    # H_1: R is a principal ideal domain
    h1 = False
    try:
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif str(R) == 'ZZ' or R.__class__.__name__ == 'IntegerRing':
            h1 = True
        elif str(R) == 'QQ[x]':
            h1 = True
    except Exception:
        pass

    # ¬Q: R is not integrally closed in K
    # We look for an element in K that is integral over R but not in R.
    neg_q = False
    try:
        x_sym = Symbol('x')
        
        if K is not None:
            if isinstance(K, (list, tuple, set)):
                thetas = list(K)
            else:
                thetas = [K]
                
            found = False
            for K_elem in thetas:
                if hasattr(K_elem, 'ext'):
                    try:
                        theta = K_elem.ext.as_expr()
                    except Exception:
                        theta = K_elem.ext
                else:
                    theta = K_elem
                
                # Search for an element (a + b*theta)/d in K \ R that is integral over R
                for d in range(1, 6):
                    for a in range(-5, 6):
                        for b in range(-5, 6):
                            if b == 0 and d == 1:
                                continue
                            try:
                                elem = (a + b * theta) / d
                                mp = minpoly(elem, x_sym)
                                
                                # Currently we specifically support checking integrality over ZZ
                                if str(R) == 'ZZ' or R.__class__.__name__ == 'IntegerRing':
                                    coeffs = mp.as_poly(x_sym).coeffs()
                                    # An element is integral over ZZ iff its minimal monic polynomial over QQ has integer coefficients
                                    if all(c.is_integer for c in coeffs):
                                        # Check if the element is strictly outside of ZZ
                                        if not elem.is_integer:
                                            found = True
                                            break
                            except Exception:
                                pass
                        if found: break
                    if found: break
                if found: break
            neg_q = found
    except Exception:
        pass

    return [h1, neg_q]