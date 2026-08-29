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
    "H_1: P is a prime ideal of R",
    "H_2: f(x) is a polynomial over R of degree n >= 1",
    "H_3: a_n is not an element of P",
    "H_4: a_i is an element of P for all 0 <= i < n",
    "H_5: a_0 is not an element of the ideal P^2",
    "¬Q: f(x) can be expressed as the product of two polynomials over R of strictly positive degree"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        R = witness['R']
        add = witness['add']
        mul = witness['mul']
        zero = witness['zero']
        one = witness['one']
        P = witness['P']
        f = witness['f']
        g = witness['g']
        h = witness['h']
    except Exception:
        return [False] * 6

    if not isinstance(R, (list, tuple, set)) or len(R) > 100:
        return [False] * 6

    # H_1: P is a prime ideal of R
    try:
        h1 = True
        if not all(p in R for p in P):
            h1 = False
        
        if zero not in R or one not in R:
            h1 = False
        if zero == one:
            h1 = False
            
        for a in R:
            if add(a, zero) != a: h1 = False
            if mul(a, one) != a: h1 = False
            if mul(one, a) != a: h1 = False
            
            has_inv = False
            for b in R:
                sum_ab = add(a, b)
                mul_ab = mul(a, b)
                if sum_ab not in R: h1 = False
                if mul_ab not in R: h1 = False
                if sum_ab == zero:
                    has_inv = True
                if sum_ab != add(b, a): h1 = False
                if mul_ab != mul(b, a): h1 = False
            if not has_inv:
                h1 = False
                
            for b in R:
                for c in R:
                    if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
        
        if zero not in P:
            h1 = False
        for p1 in P:
            has_inv = False
            for p2 in P:
                sum_p = add(p1, p2)
                if sum_p == zero:
                    has_inv = True
                if sum_p not in P:
                    h1 = False
            if not has_inv:
                h1 = False
                
        for r in R:
            for p in P:
                if mul(r, p) not in P:
                    h1 = False
        
        if len(P) == len(R):
            h1 = False
            
        for a in R:
            for b in R:
                if mul(a, b) in P:
                    if a not in P and b not in P:
                        h1 = False
    except Exception:
        h1 = False

    # H_2: f(x) is a polynomial over R of degree n >= 1
    try:
        h2 = True
        if not isinstance(f, (list, tuple)):
            h2 = False
        elif not all(c in R for c in f):
            h2 = False
        else:
            deg_f = -1
            for i, c in enumerate(f):
                if c != zero:
                    deg_f = i
            if deg_f < 1:
                h2 = False
    except Exception:
        h2 = False

    # H_3: a_n is not an element of P
    try:
        if h2:
            a_n = f[deg_f]
            h3 = a_n not in P
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: a_i is an element of P for all 0 <= i < n
    try:
        if h2:
            h4 = all(f[i] in P for i in range(deg_f))
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: a_0 is not an element of the ideal P^2
    try:
        if h2:
            P2 = []
            for p1 in P:
                for p2 in P:
                    prod = mul(p1, p2)
                    if prod not in P2:
                        P2.append(prod)
            
            added = True
            while added:
                added = False
                new_elements = []
                for x in P2:
                    for y in P2:
                        s = add(x, y)
                        if s not in P2 and s not in new_elements:
                            new_elements.append(s)
                if new_elements:
                    P2.extend(new_elements)
                    added = True
            a_0 = f[0]
            h5 = a_0 not in P2
        else:
            h5 = False
    except Exception:
        h5 = False

    # ¬Q: f(x) can be expressed as the product of two polynomials over R of strictly positive degree
    try:
        neg_Q = True
        if not isinstance(g, (list, tuple)) or not isinstance(h, (list, tuple)):
            neg_Q = False
        elif not all(c in R for c in g) or not all(c in R for c in h):
            neg_Q = False
        else:
            deg_g = -1
            for i, c in enumerate(g):
                if c != zero:
                    deg_g = i
            deg_h = -1
            for i, c in enumerate(h):
                if c != zero:
                    deg_h = i
            
            if deg_g < 1 or deg_h < 1:
                neg_Q = False
            else:
                prod_deg = deg_g + deg_h
                prod = [zero] * (prod_deg + 1)
                for i in range(deg_g + 1):
                    for j in range(deg_h + 1):
                        term = mul(g[i], h[j])
                        prod[i+j] = add(prod[i+j], term)
                
                len_max = max(deg_f + 1, prod_deg + 1)
                f_ext = list(f[:deg_f+1]) + [zero] * (len_max - (deg_f + 1))
                prod_ext = list(prod) + [zero] * (len_max - len(prod))
                
                for i in range(len_max):
                    if f_ext[i] != prod_ext[i]:
                        neg_Q = False
                        break
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_Q)]