import sympy
from sympy import Symbol, Poly, S
from sympy.polys.domains import ZZ, QQ, RR, CC, Domain

x, y, z = sympy.symbols('x y z')

def get_domain(R):
    if R == S.Integers:
        return ZZ
    if R == S.Rationals:
        return QQ
    if R == S.Reals:
        return RR
    if R == S.Complexes:
        return CC
    return R

def get_x(f, g):
    gens = set()
    if hasattr(f, 'free_symbols'):
        gens.update(f.free_symbols)
    if hasattr(g, 'free_symbols'):
        gens.update(g.free_symbols)
    if gens:
        return sorted(list(gens), key=lambda s: s.name)[0]
    return Symbol('x')

def conditions(witness):
    try:
        if len(witness) == 4:
            R_in, f, g, x_sym = witness
            R = get_domain(R_in)
        elif len(witness) == 3:
            R_in, f, g = witness
            R = get_domain(R_in)
            x_sym = get_x(f, g)
        elif len(witness) == 2:
            f, g = witness
            R = Poly(f).domain
            x_sym = get_x(f, g)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = False
        if isinstance(R, Domain):
            if R.is_Field or R == ZZ:
                h1 = True
            elif hasattr(R, 'domain') and R.is_PolynomialRing:
                base = R.domain
                if base.is_Field or base == ZZ:
                    h1 = True
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x_sym)
        poly_g = Poly(g, x_sym)
        
        h2 = False
        if poly_f.LC() == 1 and poly_g.LC() == 1:
            h2 = True
            for c in poly_f.coeffs():
                if c not in R:
                    h2 = False
                    break
            if h2:
                for c in poly_g.coeffs():
                    if c not in R:
                        h2 = False
                        break
    except Exception:
        h2 = False

    try:
        K = R.get_field()
        poly_f_K = Poly(f, x_sym, domain=K)
        poly_g_K = Poly(g, x_sym, domain=K)
        q_K, r_K = poly_g_K.div(poly_f_K)
        h3 = r_K.is_zero
    except Exception:
        h3 = False

    try:
        poly_f_R = Poly(f, x_sym, domain=R)
        poly_g_R = Poly(g, x_sym, domain=R)
        q_R, r_R = poly_g_R.div(poly_f_R)
        neg_q = not r_R.is_zero
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integrally closed integral domain",
    "H_2: f and g are monic polynomials over R",
    "H_3: f divides g in the polynomial ring over K",
    "¬Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 3
NEG_Q_INDEX = 3