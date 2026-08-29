import sympy
from sympy import Poly, minimal_polynomial
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: E is the normal closure of Q(alpha) over Q",
    "not Q: The degree of E over Q is not a power of 2, or Gal is not a 2-group"
]

def get_min_poly(witness):
    try:
        p = Poly(witness, x, domain='QQ')
        if p.degree() > 0:
            return p.monic()
    except Exception:
        pass
        
    try:
        p_expr = minimal_polynomial(witness, x)
        p = Poly(p_expr, x, domain='QQ')
        if p.degree() > 0:
            return p.monic()
    except Exception:
        pass
        
    return None

def conditions(witness):
    try:
        p = get_min_poly(witness)
        h1 = (p is not None) and p.is_irreducible
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            n = p.degree()
            if n & (n - 1) != 0:
                neg_q = True
            elif n == 1 or n == 2:
                neg_q = False
            elif n == 4:
                coeffs = p.all_coeffs()
                b = coeffs[1]
                c = coeffs[2]
                d = coeffs[3]
                e = coeffs[4]
                
                c2 = -c
                c1 = b*d - 4*e
                c0 = -b**2 * e + 4*c*e - d**2
                
                R = Poly(x**3 + c2*x**2 + c1*x + c0, x, domain='QQ')
                roots_dict = R.ground_roots()
                
                if len(roots_dict) > 0:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]