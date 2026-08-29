import sympy
from sympy import Poly, Symbol, sqrt, I, Rational, QQ, ZZ
from sympy.abc import x

def is_splitting_field(F, f, E_gens, x_sym):
    f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
    for gen in E_gens:
        val = f_expr.subs(x_sym, gen)
        if hasattr(val, 'simplify'):
            val = val.simplify()
        if val != 0:
            return False, None
    try:
        if not E_gens:
            E = F
        else:
            E = F.algebraic_field(*E_gens)
    except Exception:
        return False, None
    try:
        poly_f_E = Poly(f_expr, x_sym, domain=E)
        factors = poly_f_E.factor_list()[1]
        splits = all(fac[0].degree() == 1 for fac in factors)
        if not splits:
            return False, E
    except Exception:
        return False, None
    return True, E

def conditions(witness):
    F = witness.get('F', QQ)
    F_prime = witness.get('F_prime', QQ)
    phi = witness.get('phi', lambda a: a)
    f = witness.get('f')
    f_prime = witness.get('f_prime')
    E_gens = witness.get('E_gens', [])
    E_prime_gens = witness.get('E_prime_gens', [])
    
    f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
    f_prime_expr = f_prime.as_expr() if hasattr(f_prime, 'as_expr') else f_prime
    
    try:
        h1 = getattr(F, 'is_Field', False) and getattr(F_prime, 'is_Field', False)
    except Exception:
        h1 = False
        
    try:
        h2 = callable(phi) and phi(F.one) == F_prime.one and phi(F.zero) == F_prime.zero
    except Exception:
        h2 = False
        
    try:
        poly_f = Poly(f_expr, x, domain=F)
        h3 = True
    except Exception:
        h3 = False
        
    try:
        h4, E = is_splitting_field(F, f_expr, E_gens, x)
    except Exception:
        h4 = False
        E = None
        
    try:
        poly_f_prime = Poly(f_prime_expr, x, domain=F_prime)
        h5_part1 = True
    except Exception:
        h5_part1 = False
        
    try:
        h5_part2, E_prime = is_splitting_field(F_prime, f_prime_expr, E_prime_gens, x)
        h5 = h5_part1 and h5_part2
    except Exception:
        h5 = False
        E_prime = None
        
    try:
        if E is None or E_prime is None:
            neg_q = False
        else:
            f_coeffs = Poly(f_expr, x, domain=F).all_coeffs()
            f_phi_coeffs = [phi(c) for c in f_coeffs]
            f_phi = Poly(f_phi_coeffs, x, domain=F_prime).as_expr()
            
            poly_f_phi_E_prime = Poly(f_phi, x, domain=E_prime)
            factors = poly_f_phi_E_prime.factor_list()[1]
            splits_f_phi = all(fac[0].degree() == 1 for fac in factors)
            
            def get_degree(domain):
                if hasattr(domain, 'mod'):
                    return domain.mod.degree()
                return 1
                
            deg_E = get_degree(E)
            deg_E_prime = get_degree(E_prime)
            
            neg_q = (not splits_f_phi) or (deg_E != deg_E_prime)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F and F prime are fields",
    "H_2: phi is a field isomorphism from F onto F prime",
    "H_3: f(x) is a polynomial over F",
    "H_4: E is a splitting field of f(x) over F",
    "H_5: E prime is a splitting field of f prime(x) over F prime",
    "¬Q: There does not exist an isomorphism tau from E onto E prime extending phi"
]

N_HYP = 5
NEG_Q_INDEX = 5