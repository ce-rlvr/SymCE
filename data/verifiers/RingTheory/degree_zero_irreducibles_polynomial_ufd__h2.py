import sympy

ZZ = sympy.ZZ
QQ = sympy.QQ

def get_domain(R):
    if R == sympy.S.Integers:
        return sympy.ZZ
    if R == sympy.S.Rationals:
        return sympy.QQ
    if R == sympy.S.Reals:
        return sympy.RR
    if R == sympy.S.Complexes:
        return sympy.CC
    return R

def is_ufd(R):
    if R == sympy.S.Integers:
        return True
    if R == sympy.S.Reals or R == sympy.S.Rationals or R == sympy.S.Complexes:
        return True
    if getattr(R, 'is_Field', False):
        return True
    if getattr(R, 'is_PID', False):
        return True
    if hasattr(R, 'is_UFD') and R.is_UFD:
        return True
    if R == sympy.ZZ or R == sympy.QQ:
        return True
    if hasattr(R, 'dom') and hasattr(R, 'gens'):
        return is_ufd(R.dom)
    return False

def check_irreducible_in_R(c, R):
    if R == sympy.ZZ:
        try:
            return sympy.isprime(abs(int(c)))
        except Exception:
            return False
    if R == sympy.QQ or getattr(R, 'is_Field', False):
        return False
    if hasattr(R, 'gens') and hasattr(R, 'dom'):
        try:
            p = sympy.Poly(c, *R.gens, domain=R.dom)
            if p.is_zero:
                return False
            if sum(p.degree_list()) == 0:
                return check_irreducible_in_R(c, R.dom)
            return p.is_irreducible
        except Exception:
            return False
    return False

def check_irreducible_in_Rx(c, R):
    try:
        x = sympy.Dummy('x')
        return sympy.Poly(c, x, domain=R).is_irreducible
    except Exception:
        return False

def conditions(witness):
    try:
        R, c = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_ufd(R))
    except Exception:
        h1 = False
        
    try:
        R_dom = get_domain(R)
        h2 = bool(c in R_dom)
    except Exception:
        h2 = False
        
    try:
        R_dom = get_domain(R)
        c_expr = sympy.sympify(c)
            
        irr_R = check_irreducible_in_R(c_expr, R_dom)
        irr_Rx = check_irreducible_in_Rx(c_expr, R_dom)
        
        neg_q = bool(irr_Rx != irr_R)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: c is an element of R",
    "neg_Q: c is irreducible in the polynomial ring over R iff c is irreducible in R is false"
]

N_HYP = 2
NEG_Q_INDEX = 2