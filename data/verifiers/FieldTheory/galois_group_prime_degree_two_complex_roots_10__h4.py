import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if isinstance(witness, tuple) or isinstance(witness, list):
            f_expr = witness[-1]
        else:
            f_expr = witness
            
        if isinstance(f_expr, sympy.Poly):
            f = f_expr
            x = f.gen
        else:
            f_expr = sympy.sympify(f_expr)
            symbols = f_expr.free_symbols
            if len(symbols) == 1:
                x = list(symbols)[0]
            else:
                x = sympy.Symbol('x')
            f = sympy.Poly(f_expr, x)
    except Exception:
        return [False, False, False, False]
        
    try:
        p = f.degree()
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    try:
        domain_ok = f.domain.is_RationalField or f.domain.is_IntegerRing
        h2 = bool(domain_ok and f.is_irreducible)
    except Exception:
        h2 = False

    try:
        real_roots_count = len(sympy.real_roots(f.as_expr()))
        h3 = bool(real_roots_count == p - 2)
    except Exception:
        h3 = False

    try:
        def is_S_p(poly, deg):
            if deg <= 1:
                return True
            if not poly.is_irreducible:
                return False
            disc = sympy.discriminant(poly)
            if disc.is_Integer and disc != 0:
                if sympy.Integer(disc).is_square:
                    return False
            elif disc.is_Rational and disc != 0:
                num, den = disc.as_numer_denom()
                if sympy.Integer(num).is_square and sympy.Integer(den).is_square:
                    return False

            if deg == 2:
                return True
            if deg == 3:
                return True
            if deg == 4:
                f_monic = poly.monic()
                coeffs = f_monic.all_coeffs()
                b, c, d, e = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
                y = sympy.Symbol('y')
                R = y**3 - c*y**2 + (b*d - 4*e)*y - b**2*e + 4*c*e - d**2
                R_poly = sympy.Poly(R, y)
                return R_poly.is_irreducible
            
            if sympy.isprime(deg) and len(sympy.real_roots(poly.as_expr())) == deg - 2:
                return True
                
            return False

        neg_q = not is_S_p(f, p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ['H_1: p is prime', 'H_2: f is irreducible of degree p', 'H_3: f has p-2 real roots', 'not_Q: Galois group is not S_p']
N_HYP = 3
NEG_Q_INDEX = 3