import sympy
import sympy.ntheory
from sympy import symbols, Matrix, Expr, Poly, eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z, t
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (q, n, alpha)
    """
    try:
        q, n, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F_q is a finite field with q elements
    # This implies q must be a prime power.
    try:
        factors = sympy.ntheory.factorint(q)
        h1 = (len(factors) == 1)
        p = list(factors.keys())[0]
    except Exception:
        h1 = False
        p = None
        
    # H_2: F_{q^n} is an extension field of degree n over F_q
    # This implies n is a positive integer. We bound it to prevent performance issues.
    try:
        h2 = isinstance(n, int) and 1 <= n <= 1000
    except Exception:
        h2 = False
        
    # ¬Q: The norm N_{F_{q^n}/F_q}(\alpha) is NOT equal to \alpha^{(q^n-1)/(q-1)}
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            exponent = (q**n - 1) // (q - 1)
            
            if getattr(alpha, 'is_Matrix', False):
                # For a matrix over F_q, the norm down to F_q is its determinant.
                norm_val = alpha.det()
                formula_val = alpha**exponent
                # A scalar determinant is not equal to a matrix.
                neg_q = norm_val != formula_val
                
            elif isinstance(alpha, Expr) and not alpha.is_number:
                # Transcendental element over F_q (e.g., a polynomial in x).
                # Since the coefficients are in F_q, the Galois conjugates are all equal to alpha.
                # Thus the norm is alpha**n.
                norm_val = sympy.cancel(alpha**n)
                formula_val = sympy.cancel(alpha**exponent)
                diff = sympy.cancel(norm_val - formula_val)
                num, den = diff.as_numer_denom()
                poly_diff = Poly(num, domain=sympy.GF(p))
                neg_q = not poly_diff.is_zero
                
            else:
                # Scalar in F_q
                try:
                    norm_val = int(alpha)**n
                    formula_val = int(alpha)**exponent
                    neg_q = (norm_val - formula_val) % p != 0
                except Exception:
                    neg_q = alpha**n != alpha**exponent
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "¬Q: The norm N_{F_{q^n}/F_q}(\alpha) is not equal to \alpha^{(q^n-1)/(q-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2