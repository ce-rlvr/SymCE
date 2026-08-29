import sympy
from sympy import Poly, simplify, sympify, ZZ, QQ
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        R, a, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    # H_2: a is an element of R
    try:
        h2 = bool(a in R)
    except Exception:
        h2 = False
        
    # ¬Q: The content of f does not divide f(a) in R
    try:
        if not isinstance(f, Poly):
            f_poly = Poly(f)
        else:
            f_poly = f
            
        c = sympify(f_poly.content())
        
        if len(f_poly.gens) == 0:
            v = sympify(f_poly.as_expr())
        elif len(f_poly.gens) == 1:
            v = sympify(f_poly.eval(a))
        else:
            v = sympify(f_poly.as_expr().subs(f_poly.gens[0], a))
            
        if c == 0:
            divides = (v == 0)
        else:
            q = simplify(v / c)
            divides = bool(q in R)
            
        neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a is an element of R",
    "¬Q: The content of f does not divide f(a) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2