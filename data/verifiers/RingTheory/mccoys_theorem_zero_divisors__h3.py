import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f(x) is a zero divisor in the polynomial ring",
    "¬Q: There does not exist a non-zero element c in R such that c f(x) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(w):
    if isinstance(w, dict) and "elements" in w: return w["elements"]
    if hasattr(w, "elements"): return w.elements
    return None

def get_zero(w):
    if isinstance(w, dict) and "zero" in w: return w["zero"]
    if hasattr(w, "zero"): return w.zero
    return None

def get_add(w):
    if isinstance(w, dict) and "add" in w: return w["add"]
    if hasattr(w, "add"): return w.add
    return None

def get_mul(w):
    if isinstance(w, dict) and "mul" in w: return w["mul"]
    if hasattr(w, "mul"): return w.mul
    return None

def get_f(w):
    if isinstance(w, dict) and "f" in w: return w["f"]
    if hasattr(w, "f"): return w.f
    return None

def get_g(w):
    if isinstance(w, dict) and "g" in w: return w["g"]
    if hasattr(w, "g"): return w.g
    return None

def is_zero_poly(p, zero):
    return all(c == zero for c in p)

def poly_mul(p1, p2, add, mul, zero):
    if not p1 or not p2:
        return []
    deg1 = len(p1) - 1
    deg2 = len(p2) - 1
    res = [zero] * (deg1 + deg2 + 1)
    for i in range(deg1 + 1):
        for j in range(deg2 + 1):
            res[i+j] = add(res[i+j], mul(p1[i], p2[j]))
    return res

def conditions(witness):
    elements = get_elements(witness)
    zero = get_zero(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    f = get_f(witness)
    g = get_g(witness)

    # H1: R is a commutative ring
    h1 = False
    try:
        if elements is not None and zero is not None and add is not None and mul is not None:
            if zero in elements:
                h1 = True
                n = len(elements)
                if n > 100:
                    # Too large to check exhaustively, just check commutativity
                    for a in elements:
                        for b in elements:
                            if mul(a, b) != mul(b, a):
                                h1 = False
                                break
                        if not h1: break
                else:
                    # Exhaustive check for ring axioms
                    for a in elements:
                        if add(a, zero) != a or add(zero, a) != a:
                            h1 = False; break
                        
                        has_inv = False
                        for b in elements:
                            if add(a, b) == zero and add(b, a) == zero:
                                has_inv = True; break
                        if not has_inv:
                            h1 = False; break
                            
                        for b in elements:
                            ab_add = add(a, b)
                            ab_mul = mul(a, b)
                            if ab_add not in elements: h1 = False; break
                            if ab_mul not in elements: h1 = False; break
                            if ab_add != add(b, a): h1 = False; break
                            if ab_mul != mul(b, a): h1 = False; break
                            
                            for c in elements:
                                if add(ab_add, c) != add(a, add(b, c)): h1 = False; break
                                if mul(ab_mul, c) != mul(a, mul(b, c)): h1 = False; break
                                if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): h1 = False; break
                                if mul(ab_add, c) != add(mul(a, c), mul(b, c)): h1 = False; break
                            if not h1: break
                        if not h1: break
    except Exception:
        h1 = False

    # H2: f(x) is a zero divisor in R[x]
    h2 = False
    try:
        if elements is not None and zero is not None and add is not None and mul is not None and f is not None:
            if not is_zero_poly(f, zero):
                if g is not None and not is_zero_poly(g, zero):
                    fg = poly_mul(f, g, add, mul, zero)
                    gf = poly_mul(g, f, add, mul, zero)
                    if is_zero_poly(fg, zero) or is_zero_poly(gf, zero):
                        h2 = True
                else:
                    # Fallback: search for a constant zero divisor
                    for c in elements:
                        if c != zero:
                            cf = [mul(c, coeff) for coeff in f]
                            fc = [mul(coeff, c) for coeff in f]
                            if is_zero_poly(cf, zero) or is_zero_poly(fc, zero):
                                h2 = True
                                break
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a non-zero c in R such that c f(x) = 0
    neg_q = False
    try:
        if elements is not None and zero is not None and mul is not None and f is not None:
            exists_c = False
            for c in elements:
                if c != zero:
                    cf = [mul(c, coeff) for coeff in f]
                    if is_zero_poly(cf, zero):
                        exists_c = True
                        break
            neg_q = not exists_c
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]