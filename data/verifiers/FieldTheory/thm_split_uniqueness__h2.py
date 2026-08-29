import sympy
from sympy import Poly, factor, roots, Symbol
from sympy.polys.numberfields import primitive_element

# Top-level setup
QQ = sympy.QQ
x = Symbol('x')

def is_splitting_field(K, f, x_var, F):
    try:
        # A common edge case for dropped hypotheses: f(x) = 0
        # The zero polynomial splits completely in any extension field,
        # and its roots (all elements) generate the field.
        if f == 0:
            return True
            
        # Find roots of f
        rts = roots(f, x_var)
        if sum(rts.values()) < Poly(f, x_var).degree():
            return False
            
        root_list = list(rts.keys())
        
        # Compute the primitive element of the roots over F
        prim, minpoly = primitive_element(root_list, domain=F)
        deg_split = minpoly.degree()
        
        # Check if K has the same degree as the splitting field
        deg_K = K.ext.degree() if hasattr(K, 'ext') else 1
        if deg_K != deg_split:
            return False
            
        # Check if f splits completely in K
        if hasattr(K, 'ext'):
            factored = factor(f, x_var, extension=K.ext)
        else:
            factored = factor(f, x_var, domain=K)
            
        for fac, mult in factored.as_powers_dict().items():
            if Poly(fac, x_var).degree() > 1:
                return False
                
        return True
    except Exception:
        return False

def are_isomorphic(K1, K2, F):
    if K1 == K2:
        return True
    try:
        deg1 = K1.ext.degree() if hasattr(K1, 'ext') else 1
        deg2 = K2.ext.degree() if hasattr(K2, 'ext') else 1
        if deg1 != deg2:
            return False
        if deg1 == 1:
            return True
            
        # Check if K1's generator is in K2 by factoring its minimal polynomial over K2
        minpoly = K1.ext.minpoly
        factored = factor(minpoly, extension=K2.ext)
        for fac, mult in factored.as_powers_dict().items():
            if Poly(fac).degree() == 1:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K1 = witness.get('K1')
            K2 = witness.get('K2')
            f = witness.get('f')
            x_var = witness.get('x', x)
        else:
            F = witness.F
            K1 = witness.K1
            K2 = witness.K2
            f = witness.f
            x_var = getattr(witness, 'x', x)
    except Exception:
        try:
            F, K1, K2, f, x_var = witness
        except Exception:
            return [False, False, False, False]
            
    # H_1: F is a field
    try:
        h1_ok = bool(F.is_Field)
    except Exception:
        h1_ok = False
        
    # H_2: K_1 is a splitting field of f(x) over F
    try:
        h2_ok = bool(is_splitting_field(K1, f, x_var, F))
    except Exception:
        h2_ok = False
        
    # H_3: K_2 is a splitting field of f(x) over F
    try:
        h3_ok = bool(is_splitting_field(K2, f, x_var, F))
    except Exception:
        h3_ok = False
        
    # ¬Q: K_1 and K_2 are NOT isomorphic over F
    try:
        neg_q_ok = not are_isomorphic(K1, K2, F)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K_1 is a splitting field of f(x) over F",
    "H_3: K_2 is a splitting field of f(x) over F",
    "¬Q: K_1 and K_2 are not isomorphic over F"
]

N_HYP = 3
NEG_Q_INDEX = 3