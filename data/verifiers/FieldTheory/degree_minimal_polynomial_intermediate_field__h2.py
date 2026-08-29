import sympy as sp
from sympy import minpoly, Symbol
from sympy.polys.polyerrors import NotAlgebraic
from sympy.abc import x, y, z

# Top-level setup
T = Symbol('T')

def is_in_field(element, gens):
    if not gens:
        try:
            return element.is_Rational
        except Exception:
            return False
            
    if element in gens or element.is_Rational:
        return True
        
    # Check rational function
    try:
        num, den = sp.fraction(sp.cancel(element))
        if num.is_polynomial(*gens) and den.is_polynomial(*gens):
            return True
    except Exception:
        pass
        
    # Check algebraic field
    try:
        domain = sp.QQ.algebraic_field(*gens)
        domain.from_sympy(element)
        return True
    except Exception:
        pass
        
    return False

def get_minpoly_degree(element, gens):
    if not gens:
        try:
            p = minpoly(element, T, domain=sp.QQ)
            return p.as_poly(T).degree()
        except NotAlgebraic:
            return None
            
    if element in gens or element.is_Rational:
        return 1
        
    # Check if element is in QQ(gens)
    try:
        num, den = sp.fraction(sp.cancel(element))
        if num.is_polynomial(*gens) and den.is_polynomial(*gens):
            return 1
    except Exception:
        pass
        
    # Try algebraic field
    try:
        domain = sp.QQ.algebraic_field(*gens)
        p = minpoly(element, T, domain=domain)
        return p.as_poly(T).degree()
    except NotAlgebraic:
        return None
    except Exception:
        pass
        
    # Check for obvious transcendence
    gen_symbols = set()
    for g in gens:
        gen_symbols.update(g.free_symbols)
    if not element.free_symbols.issubset(gen_symbols):
        return None
        
    raise ValueError(f"Cannot compute minpoly of {element} over QQ({gens})")

def conditions(witness):
    try:
        K_gens = [sp.sympify(g) for g in witness.get('K_gens', [])]
        M_gens = [sp.sympify(g) for g in witness.get('M_gens', [])]
        L_gens = [sp.sympify(g) for g in witness.get('L_gens', [])]
        
        alpha_raw = witness.get('alpha', None)
        if alpha_raw is None:
            return [False, False]
        alpha = sp.sympify(alpha_raw)
    except Exception:
        return [False, False]
        
    # H1: K \subseteq M \subseteq L
    try:
        h1 = True
        for g in K_gens:
            if not is_in_field(g, M_gens):
                h1 = False
                break
        for g in M_gens:
            if not is_in_field(g, L_gens):
                h1 = False
                break
    except Exception:
        h1 = False
        
    # neg_Q: degree of minpoly over M <= degree of minpoly over K
    try:
        deg_M = get_minpoly_degree(alpha, M_gens)
        deg_K = get_minpoly_degree(alpha, K_gens)
        
        # If the minimal polynomial does not exist (e.g. transcendental), 
        # the degree is undefined, making the inequality false.
        if deg_M is None or deg_K is None:
            q = False
        else:
            q = (deg_M <= deg_K)
            
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K, M, and L are fields such that K \\subseteq M \\subseteq L",
    "¬Q: The degree of the minimal polynomial of \\alpha over M is NOT less than or equal to the degree of the minimal polynomial of \\alpha over K (e.g. undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1