import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

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

def conditions(witness):
    try:
        if isinstance(witness, str):
            witness = sympy.sympify(witness)
            
        if isinstance(witness, sympy.Poly):
            f = witness
            if not f.domain.is_QQ:
                f = f.set_domain('QQ')
        elif isinstance(witness, sympy.Expr):
            free_symbols = witness.free_symbols
            if len(free_symbols) == 1:
                var = list(free_symbols)[0]
            else:
                var = sympy.Symbol('x')
            f = sympy.Poly(witness, var, domain='QQ')
        else:
            return [False, False]
            
        deg = f.degree()
        if deg < 2:
            return [False, False]
            
        factors = sympy.factorint(deg)
        if len(factors) != 1:
            return [False, False]
            
        p = list(factors.keys())[0]
        n = factors[p]
        
        if not f.is_irreducible:
            return [False, False]
            
        h1 = True
        neg_q = False
        
        if n == 1:
            if p == 2:
                neg_q = False
            else:
                disc = sympy.Rational(f.discriminant())
                if not (sympy.Integer(disc.p).is_square and sympy.Integer(disc.q).is_square):
                    neg_q = True
                else:
                    real_roots = len(sympy.real_roots(f))
                    if 0 < real_roots < deg:
                        neg_q = True
                    elif p == 3:
                        neg_q = False
                    else:
                        neg_q = True
        elif n == 2 and p == 2:
            f_monic = f.monic()
            coeffs = f_monic.all_coeffs()
            a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
            y_sym = sympy.Symbol('y')
            R = sympy.Poly(y_sym**3 - b*y_sym**2 + (a*c - 4*d)*y_sym - a**2*d + 4*b*d - c**2, y_sym, domain='QQ')
            has_rat_root = len(R.ground_roots()) > 0
            neg_q = not has_rat_root
        else:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: degree of L over K is p^n for a prime p and an integer n >= 1",
    "¬Q: There is no intermediate field E between K and L such that E/K is Galois and degree of E over K is p"
]

N_HYP = 1
NEG_Q_INDEX = 1