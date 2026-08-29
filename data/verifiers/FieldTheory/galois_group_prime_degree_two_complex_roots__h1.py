import sympy
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_galois_group_Sn(f_expr, x_sym):
    f_poly = sympy.Poly(f_expr, x_sym)
    if f_poly.domain not in (sympy.QQ, sympy.ZZ):
        return False
    n = f_poly.degree()
    if n <= 1:
        return True
    if not f_poly.is_irreducible:
        return False
        
    disc = f_poly.discriminant()
    if disc == 0:
        return False
    if n >= 2 and sympy.sqrt(disc).is_rational:
        return False
        
    if n == 2:
        return True
    if n == 3:
        return True
        
    if n == 4:
        f_monic = f_poly.monic()
        coeffs = f_monic.all_coeffs()
        a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
        y = sympy.Symbol('y')
        resolvent = y**3 - b*y**2 + (a*c - 4*d)*y - a**2*d + 4*b*d - c**2
        res_poly = sympy.Poly(resolvent, y)
        return res_poly.is_irreducible

    from sympy.ntheory import primerange
    primes = list(primerange(n + 1, 2000))
    
    transposition = tuple([1]*(n-2) + [2])
    n_minus_1_cycle = tuple([1] + [n-1])
    
    seen_transposition = False
    seen_n_minus_1 = False
    
    for p in primes:
        try:
            f_mod = sympy.Poly(f_expr, x_sym, modulus=p)
            if f_mod.degree() != n:
                continue
            if not sympy.gcd(f_mod, f_mod.diff()).is_constant():
                continue
            factors = f_mod.factor_list()[1]
            cycle = tuple(sorted([poly.degree() for poly, mult in factors]))
            if cycle == transposition:
                seen_transposition = True
            elif cycle == n_minus_1_cycle:
                seen_n_minus_1 = True
                
            if seen_transposition and seen_n_minus_1:
                return True
        except Exception:
            pass
            
    return False

def conditions(witness):
    try:
        expr = witness.as_expr() if hasattr(witness, 'as_expr') else witness
        free_symbols = expr.free_symbols
        if len(free_symbols) != 1:
            return [False, False, False, False]
        x_sym = list(free_symbols)[0]
        f_poly = sympy.Poly(expr, x_sym)
    except Exception:
        return [False, False, False, False]
        
    try:
        if f_poly.domain not in (sympy.QQ, sympy.ZZ):
            h1 = False
        else:
            h1 = f_poly.is_irreducible
    except Exception:
        h1 = False
        
    try:
        rr = sympy.real_roots(expr)
        h2 = (f_poly.degree() - len(rr) == 2)
    except Exception:
        h2 = False
        
    h3 = True
    
    try:
        is_Sn = is_galois_group_Sn(expr, x_sym)
        neg_q = not is_Sn
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial over Q",
    "H_2: f(x) has exactly two non-real roots in C",
    "H_3: L is the splitting field of f(x) over Q",
    "¬Q: The Galois group Gal(L/Q) is NOT isomorphic to S_p"
]

N_HYP = 3
NEG_Q_INDEX = 3