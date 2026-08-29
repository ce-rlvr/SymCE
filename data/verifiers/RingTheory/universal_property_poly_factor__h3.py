import sympy
from sympy import Matrix, eye, zeros
import itertools
import math
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 4:
            R, f, A, eta = witness
        elif len(witness) == 3:
            R, f, A = witness
            eta = lambda x: x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    def eq(x, y):
        try:
            return bool(x == y)
        except Exception:
            return False

    try:
        h1 = True
        for r1 in R:
            for r2 in R:
                if not eq(r1 * r2, r2 * r1):
                    h1 = False
                    break
            if not h1: break
            
        if h1:
            for r1 in R:
                for r2 in R:
                    if not any(eq(r1 + r2, r) for r in R):
                        h1 = False
                        break
                    if not any(eq(r1 * r2, r) for r in R):
                        h1 = False
                        break
                    if not any(eq(r1 - r2, r) for r in R):
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            has_id = False
            for e in R:
                is_id = True
                for r in R:
                    if not eq(e * r, r) or not eq(r * e, r):
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            if not has_id:
                h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        if isinstance(f, dict):
            if not f:
                coeffs = []
            else:
                max_deg = max(f.keys())
                zero_R = None
                for r in R:
                    if all(eq(r + x, x) for x in R):
                        zero_R = r
                        break
                coeffs = [f.get(i, zero_R) for i in range(max_deg + 1)]
        else:
            coeffs = list(f)
            
        for c in coeffs:
            if not any(eq(c, r) for r in R):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        zero = None
        for z in A:
            if all(eq(z + x, x) for x in A):
                zero = z
                break
                
        if zero is None:
            neg_q = False
        else:
            one = None
            for e in A:
                if all(eq(e * x, x) and eq(x * e, x) for x in A):
                    one = e
                    break
                    
            if one is None:
                neg_q = False
            else:
                def eval_poly(poly, a):
                    res = zero
                    a_pow = one
                    for c in poly:
                        res = res + eta(c) * a_pow
                        a_pow = a_pow * a
                    return res
                    
                roots = []
                for a in A:
                    if eq(eval_poly(coeffs, a), zero):
                        roots.append(a)
                        
                hom_roots = []
                for a in roots:
                    if all(eq(a * eta(r), eta(r) * a) for r in R):
                        hom_roots.append(a)
                        
                neg_q = len(roots) != len(hom_roots)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial over R",
    "¬Q: The set of R-algebra homomorphisms to A is not in natural bijection with roots of f in A"
]

N_HYP = 2
NEG_Q_INDEX = 2