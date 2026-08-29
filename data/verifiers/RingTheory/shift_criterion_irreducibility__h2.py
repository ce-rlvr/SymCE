import sympy
from sympy import Symbol, S, Poly
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_domain(R):
    if R == S.Integers: return sympy.ZZ
    if R == S.Rationals: return sympy.QQ
    if R == S.Reals: return sympy.RR
    if R == S.Complexes: return sympy.CC
    return R

def is_integral_domain(R):
    domain = get_domain(R)
    if domain in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC):
        return True
    if hasattr(domain, 'is_Field') and domain.is_Field:
        return True
    if hasattr(domain, 'mod'):
        return sympy.isprime(domain.mod)
    return False

def in_domain(c, R):
    domain = get_domain(R)
    try:
        if domain == sympy.ZZ:
            return S(c).is_integer
        if domain == sympy.QQ:
            return S(c).is_rational
        if domain == sympy.RR:
            return S(c).is_real
        if domain == sympy.CC:
            return S(c).is_complex
        if hasattr(domain, '__contains__'):
            return c in domain
    except Exception:
        pass
    return False

def check_irreducible(expr, x, domain):
    try:
        if hasattr(expr, 'as_expr'):
            expr = expr.as_expr()
        p = Poly(expr, x, domain=domain)
        return bool(p.is_irreducible)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 3:
            R, c, f = witness
            symbols = list(f.free_symbols) if hasattr(f, 'free_symbols') else []
            x = symbols[0] if symbols else Symbol('x')
        elif len(witness) == 4:
            R, c, f, x = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    domain = get_domain(R)

    try:
        h1 = is_integral_domain(R)
    except Exception:
        h1 = False

    try:
        h2 = in_domain(c, R)
    except Exception:
        h2 = False

    try:
        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
        else:
            f_expr = f
            
        f_is_irred = check_irreducible(f_expr, x, domain)
        f_c = f_expr.subs(x, x + c)
        f_c_is_irred = check_irreducible(f_c, x, domain)
        
        neg_q = bool(f_is_irred != f_c_is_irred)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: c is an element of R",
    "¬Q: f is irreducible is not equivalent to f shifted is irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2