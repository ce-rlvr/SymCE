import sympy
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup for potential witness elements
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
    # H1: R and S are rings
    try:
        R = list(witness.R)
        R_add = witness.R_add
        R_mul = witness.R_mul
        R_zero = witness.R_zero
        
        S = list(witness.S)
        S_add = witness.S_add
        S_mul = witness.S_mul
        S_zero = witness.S_zero
        
        def is_ring(elements, add, mul, zero):
            if zero not in elements: return False
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a: return False
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: return False
                for b in elements:
                    if add(a, b) != add(b, a): return False
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            return True

        h1 = is_ring(R, R_add, R_mul, R_zero) and is_ring(S, S_add, S_mul, S_zero)
    except Exception:
        h1 = False

    # H2: F is the induced ring homomorphism from R[x] to S[x] that applies f to the coefficients of polynomials
    try:
        R = list(witness.R)
        S_zero = witness.S_zero
        f = witness.f
        F = witness.F
        
        def strip_zeros(poly, zero):
            try:
                res = list(poly)
            except TypeError:
                res = [poly]
            while res and res[-1] == zero:
                res.pop()
            if not res:
                return [zero]
            return res

        h2 = True
        for a in R:
            for b in R:
                poly = [a, b]
                expected = [f(a), f(b)]
                res = F(poly)
                if strip_zeros(res, S_zero) != strip_zeros(expected, S_zero):
                    h2 = False
                    break
            if not h2:
                break
                
        if h2:
            subset_R = R[:5] if len(R) > 5 else R
            for a in subset_R:
                for b in subset_R:
                    for c in subset_R:
                        poly = [a, b, c]
                        expected = [f(a), f(b), f(c)]
                        res = F(poly)
                        if strip_zeros(res, S_zero) != strip_zeros(expected, S_zero):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # ¬Q: The kernel of F is not the ideal of R[x] consisting of all polynomials whose coefficients all belong to the kernel of f
    try:
        R = list(witness.R)
        R_add = witness.R_add
        R_mul = witness.R_mul
        R_zero = witness.R_zero
        S_zero = witness.S_zero
        f = witness.f
        
        # The set of polynomials with coefficients in ker(f) is an ideal of R[x] iff ker(f) is an ideal of R.
        # If ker(f) is not an ideal, the conclusion fails.
        K_f = [a for a in R if f(a) == S_zero]
        
        is_ideal = True
        if not K_f:
            is_ideal = False
        else:
            for a in K_f:
                inv_a = None
                for b in R:
                    if R_add(a, b) == R_zero and R_add(b, a) == R_zero:
                        inv_a = b
                        break
                if inv_a not in K_f:
                    is_ideal = False
                    break
                    
                for b in K_f:
                    if R_add(a, b) not in K_f:
                        is_ideal = False
                        break
                if not is_ideal: break
                
                for r in R:
                    if R_mul(a, r) not in K_f:
                        is_ideal = False
                        break
                    if R_mul(r, a) not in K_f:
                        is_ideal = False
                        break
                if not is_ideal: break
                
        neg_q = not is_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: F is the induced ring hom from R polys to S polys",
    "¬Q: ker(F) is not the ideal of polys with coeffs in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2