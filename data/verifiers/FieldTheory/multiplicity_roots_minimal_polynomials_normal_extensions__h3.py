import sympy
from sympy import factor_list, Poly
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

# Top-level setup
# (No specific named objects required for this field theory conjecture, 
# but x is provided for polynomial expressions)

def is_normal_extension(L_gens, K_gens):
    try:
        if not L_gens:
            L_gens = [sympy.Integer(0)]
            
        prim_L, p_Q_poly = primitive_element(L_gens, x)
        p_Q = p_Q_poly.as_expr()
        
        if K_gens:
            prim_K, _ = primitive_element(K_gens, x)
            deg_L = p_Q_poly.degree()
            prim_LK, prim_LK_poly = primitive_element(list(L_gens) + list(K_gens), x)
            deg_LK = prim_LK_poly.degree()
            if deg_L != deg_LK:
                return False
        
        if K_gens:
            factors_K = factor_list(p_Q, extension=K_gens)[1]
            p_K = None
            for fac, _ in factors_K:
                val = complex(fac.subs(x, prim_L).evalf())
                if abs(val) < 1e-7:
                    p_K = fac
                    break
            if p_K is None:
                return False
        else:
            p_K = p_Q
            
        factors_L = factor_list(p_K, extension=L_gens)[1]
        for fac, _ in factors_L:
            if Poly(fac, x).degree() > 1:
                return False
        return True
    except Exception:
        return False

def is_in_field(alpha, L_gens):
    try:
        if not L_gens:
            L_gens = [sympy.Integer(0)]
            
        prim_L, p_L_poly = primitive_element(L_gens, x)
        deg_L = p_L_poly.degree()
        
        prim_L_alpha, p_L_alpha_poly = primitive_element(list(L_gens) + [alpha], x)
        deg_L_alpha = p_L_alpha_poly.degree()
        
        return deg_L == deg_L_alpha
    except Exception:
        return False

def neg_Q_check(f, L_gens):
    try:
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
            
        if not L_gens:
            L_gens = [sympy.Integer(0)]
            
        factors_L = factor_list(f, extension=L_gens)[1]
        
        linear_exponents = []
        for fac, exp in factors_L:
            if Poly(fac, x).degree() == 1:
                linear_exponents.append(exp)
                
        if not linear_exponents:
            return False
            
        first_exp = linear_exponents[0]
        for exp in linear_exponents[1:]:
            if exp != first_exp:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    """
    witness can be a dictionary, an object, or a tuple (L_gens, K_gens, alpha, f).
    L_gens: list of generators for field L over Q
    K_gens: list of generators for field K over Q
    alpha: an element to check if it belongs to L
    f: a polynomial in x
    """
    if isinstance(witness, dict):
        L_gens = witness.get('L_gens', [])
        K_gens = witness.get('K_gens', [])
        alpha = witness.get('alpha', sympy.Integer(0))
        f = witness.get('f', x)
    elif isinstance(witness, tuple) and len(witness) == 4:
        L_gens, K_gens, alpha, f = witness
    else:
        L_gens = getattr(witness, 'L_gens', [])
        K_gens = getattr(witness, 'K_gens', [])
        alpha = getattr(witness, 'alpha', sympy.Integer(0))
        f = getattr(witness, 'f', x)
        
    if not isinstance(L_gens, (list, tuple)):
        L_gens = [L_gens]
    if not isinstance(K_gens, (list, tuple)):
        K_gens = [K_gens]
        
    L_gens = list(L_gens)
    K_gens = list(K_gens)
        
    h1 = is_normal_extension(L_gens, K_gens)
    h2 = is_in_field(alpha, L_gens)
    nq = neg_Q_check(f, L_gens)
    
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: L/K is a normal extension",
    "H_2: α is an element of L",
    "¬Q: In the prime factorization of f(x) over L, not every distinct linear factor appears with the same exponent"
]

N_HYP = 2
NEG_Q_INDEX = 2