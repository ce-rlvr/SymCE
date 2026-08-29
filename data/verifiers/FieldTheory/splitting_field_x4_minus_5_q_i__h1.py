import sympy
from sympy import QQ, I, Rational
from sympy.abc import x

# Top-level setup
# The witness is expected to be a list of sympy expressions representing the generators of F over Q.
# For example, witness = [] represents F = Q.
# witness = [I] represents F = Q(i).

def get_degree(gens):
    if not gens:
        return 1
    try:
        from sympy.polys.numberfields import primitive_element
        from sympy.abc import x
        poly = primitive_element(gens, x)
        if isinstance(poly, tuple):
            poly = poly[0]
        return poly.degree()
    except Exception:
        pass
    
    try:
        K = QQ.algebraic_field(*gens)
        if hasattr(K, 'degree'):
            return K.degree()
        if hasattr(K, 'ext') and hasattr(K.ext, 'degree'):
            return K.ext.degree()
    except Exception:
        pass
    return None

def get_gens(witness):
    if witness == QQ:
        return []
    if isinstance(witness, list):
        return witness
    if isinstance(witness, tuple):
        return list(witness)
    return [witness]

def conditions(witness):
    try:
        gens = get_gens(witness)
        deg_F = get_degree(gens)
    except Exception:
        return [False, False, False]
        
    # H1 and H2 are definitional and hold as long as F is a valid algebraic number field.
    h1 = (deg_F is not None)
    h2 = (deg_F is not None)
    
    if not h1:
        return [False, False, False]
        
    try:
        a = 5**Rational(1,4)
        
        # Compute degrees of F(a) and E = F(a, i) over Q
        deg_Fa = get_degree(gens + [a])
        deg_E = get_degree(gens + [a, I])
        
        if deg_Fa is None or deg_E is None:
            return [h1, h2, False]
            
        # [E : F] = [E : Q] / [F : Q]
        deg_E_over_F = deg_E // deg_F
        
        # E == F(a) if and only if their degrees over Q are equal
        E_eq_Fa = (deg_E == deg_Fa)
        
        conclusion = (deg_E_over_F == 4) and E_eq_Fa
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: f(x) = x^4 - 5 is in F', 'H_2: E is the splitting field of f(x) over F', '¬Q: degree of E over F is not 4 or E is not F(5**(1/4))']

N_HYP = 2
NEG_Q_INDEX = 2