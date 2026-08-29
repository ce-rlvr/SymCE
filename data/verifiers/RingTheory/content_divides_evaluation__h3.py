import sympy
from sympy import Poly, ZZ, QQ, sympify
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        R, f, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # H_2: f is a polynomial over R
    try:
        if isinstance(f, Poly):
            p = f
        else:
            p = Poly(f, x)
            
        if len(p.free_symbols) > 1:
            h2 = False
        else:
            h2 = all(c in R for c in p.coeffs())
    except Exception:
        h2 = False
        
    # ¬Q: The content of f does not divide f(a) in R
    try:
        if isinstance(f, Poly):
            p = f
            c = p.content()
            if len(p.free_symbols) == 1:
                v = p.eval(a)
            else:
                v = p.coeffs()[0] if p.coeffs() else 0
        else:
            p = Poly(f, x)
            c = p.content()
            free = list(f.free_symbols)
            if len(free) >= 1:
                v = f.subs(free[0], a)
            else:
                v = f
                
        v = sympify(v)
        c = sympify(c)
        
        if v not in R:
            divides = False
        else:
            if c == 0:
                divides = (v == 0)
            else:
                quotient = v / c
                divides = (quotient in R)
                
        neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a polynomial over R",
    "¬Q: The content of f does not divide f(a) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2