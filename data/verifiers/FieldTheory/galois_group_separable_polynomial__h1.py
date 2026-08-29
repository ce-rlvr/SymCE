import sympy
from sympy import Poly
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = ['H_1: f is separable', 'H_2: L is splitting field', 'H_3: R is roots', 'not Q: Gal does not act faithfully']

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_expr = witness[0]
        else:
            f_expr = witness
            
        f_expr = sympy.sympify(f_expr)
        f = Poly(f_expr, x)
        
        try:
            f_diff = f.diff()
            if f_diff.is_zero:
                h1 = False
            else:
                gcd_poly = f.gcd(f_diff)
                h1 = (f.degree() > 0) and (gcd_poly.degree() == 0)
        except Exception:
            h1 = False
            
        h2 = True
        h3 = True
        neg_q = False
        
        return [bool(h1), h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]