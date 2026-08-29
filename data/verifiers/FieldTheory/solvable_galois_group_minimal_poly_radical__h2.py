import sympy
from sympy import Poly
import sympy.ntheory
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

def conditions(witness):
    try:
        expr = sympy.sympify(witness)
        if isinstance(expr, sympy.Equality):
            expr = expr.lhs - expr.rhs
        symbols = list(expr.free_symbols)
        if len(symbols) == 1:
            sym = symbols[0]
        elif len(symbols) == 0:
            sym = sympy.Symbol('x')
        else:
            return [False, False, False, False, False]
            
        p = Poly(expr, sym, domain='QQ')
        h1 = True
    except Exception:
        h1 = False
        p = None

    try:
        h2 = p.degree() >= 1 if p is not None else False
    except Exception:
        h2 = False

    try:
        h3 = p.is_irreducible if p is not None else False
    except Exception:
        h3 = False

    h4 = h1 and h2

    neg_q = False
    try:
        if p is not None:
            deg = p.degree()
            if deg >= 5 and p.is_irreducible:
                if sympy.ntheory.isprime(deg):
                    real_roots = len(sympy.real_roots(p))
                    if real_roots == deg - 2:
                        neg_q = True
                
                if not neg_q and deg == 5:
                    coeffs = p.all_coeffs()
                    if coeffs[1] == 0 and coeffs[2] == 0 and coeffs[3] == 0:
                        a = coeffs[4] / coeffs[0]
                        b = coeffs[5] / coeffs[0]
                        z = sympy.Symbol('z')
                        R = (z**6 + 8*a*z**5 + 40*a**2*z**4 + 160*a**3*z**3 + 
                             400*a**4*z**2 + (512*a**5 - 3125*b**4)*z + 
                             (256*a**6 - 9375*a*b**4))
                        R_poly = Poly(R, z, domain='QQ')
                        rat_roots = [r for r in sympy.roots(R_poly).keys() if r.is_rational]
                        if not rat_roots:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: alpha in K",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "H_4: L is the splitting field of m(x) over F",
    "¬Q: The Galois group Gal(L/F) is not a solvable group"
]

N_HYP = 4
NEG_Q_INDEX = 4