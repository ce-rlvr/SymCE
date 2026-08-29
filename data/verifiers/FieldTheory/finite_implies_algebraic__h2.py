import sympy
from sympy import Symbol, QQ, ZZ, RR, CC, minpoly

# Top-level setup for potential witness expressions
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If L/K is a field extension, then every element of L is algebraic over K."
    
    The witness should be a tuple (L, K) or (L, K, alpha) where:
      - L and K are sympy domains (e.g., QQ.frac_field(x), QQ, RR, CC)
      - alpha is an optional element in L that is transcendental over K.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                L, K, alpha = witness
            elif len(witness) == 2:
                L, K = witness
                alpha = None
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # Check H_1: L/K is a field extension
    try:
        if getattr(L, 'is_Field', False) and getattr(K, 'is_Field', False):
            # L.unify(K) == L implies K is a sub-domain (subfield) of L
            if L.unify(K) == L:
                h1 = True
    except Exception:
        h1 = False
        
    # Check ¬Q: There exists an element in L that is NOT algebraic over K
    try:
        if alpha is not None:
            # Verify alpha is in L
            try:
                val = sympy.sympify(alpha)
                try:
                    L.from_sympy(val)
                    alpha_in_L = True
                except Exception:
                    if hasattr(L, 'gens') and val in L.gens:
                        alpha_in_L = True
                    else:
                        alpha_in_L = False
            except Exception:
                alpha_in_L = False
                
            if alpha_in_L:
                try:
                    # minpoly raises NotAlgebraic if the element is transcendental
                    minpoly(alpha, domain=K)
                except Exception:
                    neg_q = True
        else:
            # If alpha is not provided, try to find a transcendental element in L
            if hasattr(L, 'gens'):
                for g in L.gens:
                    try:
                        minpoly(g, domain=K)
                    except Exception:
                        neg_q = True
                        break
            # Fallback for standard continuous fields
            if not neg_q and (L == RR or L == CC):
                try:
                    minpoly(sympy.pi, domain=K)
                except Exception:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "¬Q: Every element of L is algebraic over K fails (there is a transcendental element)"
]

N_HYP = 1
NEG_Q_INDEX = 1