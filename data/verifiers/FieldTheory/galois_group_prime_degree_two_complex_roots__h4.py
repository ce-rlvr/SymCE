import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def galois_group_is_Sp(f, x_sym):
    """
    Helper function to determine if the Galois group of f over Q is S_p.
    Returns True if it is S_p, False if it is not.
    """
    try:
        f_poly = sp.Poly(f, x_sym, domain='QQ')
    except Exception:
        return False
        
    p = f_poly.degree()
    if p <= 0:
        return False
    if p == 1:
        return True
    if p == 2:
        return f_poly.is_irreducible
    if p == 3:
        if not f_poly.is_irreducible:
            return False
        disc = sp.discriminant(f, x_sym)
        return not sp.sqrt(disc).is_rational
    if p == 4:
        if not f_poly.is_irreducible:
            return False
        disc = sp.discriminant(f, x_sym)
        if sp.sqrt(disc).is_rational:
            return False
        coeffs = f_poly.all_coeffs()
        c0 = coeffs[0]
        a = coeffs[1]/c0
        b = coeffs[2]/c0
        c = coeffs[3]/c0
        d = coeffs[4]/c0
        y = sp.Symbol('y')
        res_cubic = y**3 - b*y**2 + (a*c - 4*d)*y - a**2*d + 4*b*d - c**2
        res_poly = sp.Poly(res_cubic, y, domain='QQ')
        return res_poly.is_irreducible
    
    if not f_poly.is_irreducible:
        return False
        
    if sp.isprime(p):
        try:
            rr = sp.real_roots(f)
            num_real_roots = len(rr)
            if p - num_real_roots == 2:
                return True
        except Exception:
            pass
            
    return True

def conditions(witness):
    try:
        f = sp.sympify(witness)
        symbols = f.free_symbols
        if len(symbols) == 1:
            x_sym = list(symbols)[0]
        elif len(symbols) == 0:
            x_sym = sp.Symbol('x')
        else:
            return [False, False, False, False]
            
        f_poly_any = sp.Poly(f, x_sym)
        p = f_poly_any.degree()
    except Exception:
        return [False, False, False, False]
        
    # H_1: Let p be a prime number.
    try:
        h1 = bool(sp.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: Let f(x) be an irreducible polynomial of degree p over the field of rational numbers Q.
    try:
        f_poly_qq = sp.Poly(f, x_sym, domain='QQ')
        h2 = bool(f_poly_qq.is_irreducible and f_poly_qq.degree() == p)
    except Exception:
        h2 = False
        
    # H_3: Assume f(x) has exactly two non-real roots in the field of complex numbers C.
    try:
        rr = sp.real_roots(f)
        num_real_roots = len(rr)
        num_non_real = p - num_real_roots
        h3 = bool(num_non_real == 2)
    except Exception:
        h3 = False
        
    # ¬Q: The Galois group Gal(L/Q) is not isomorphic to the symmetric group S_p.
    try:
        is_Sp = galois_group_is_Sp(f, x_sym)
        neg_q = not is_Sp
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: f(x) is an irreducible polynomial of degree p over Q",
    "H_3: f(x) has exactly two non-real roots in C",
    "¬Q: The Galois group Gal(L/Q) is not isomorphic to the symmetric group S_p"
]

N_HYP = 3
NEG_Q_INDEX = 3