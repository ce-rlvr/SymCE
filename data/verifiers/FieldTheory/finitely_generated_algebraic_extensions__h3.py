import sympy
import sympy.abc
from sympy.polys.domains import QQ, ZZ

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Finitely generated field extensions are finite."
    
    Expected witness format: (K, L, generators)
    where K and L are sympy.polys.domains.Domain objects (e.g., QQ, QQ.frac_field(x)),
    and generators is a list of elements generating L over K.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, L, generators = witness
    except Exception:
        return [False, False, False]

    # H_1: L/K is a field extension
    try:
        h1 = getattr(K, 'is_Field', False) and getattr(L, 'is_Field', False)
        
        try:
            is_subfield = (K.unify(L) == L)
        except Exception:
            is_subfield = False
            
        if not is_subfield:
            if hasattr(L, 'domain') and L.domain == K:
                is_subfield = True
            elif L == K:
                is_subfield = True
                
        h1 = bool(h1 and is_subfield)
    except Exception:
        h1 = False

    # H_2: There exists a finite set of elements such that L = K(alpha_1, ..., alpha_n)
    try:
        h2 = False
        if isinstance(generators, (list, tuple, set)):
            if len(generators) == 0:
                h2 = (L == K)
            else:
                try:
                    if L == K.frac_field(*generators):
                        h2 = True
                except Exception:
                    pass
                try:
                    if L == K.algebraic_field(*generators):
                        h2 = True
                except Exception:
                    pass
    except Exception:
        h2 = False

    # ¬Q: The field extension L/K is not finite
    # A finitely generated extension is infinite if it is a transcendental extension 
    # (i.e., a fraction field with at least one generator).
    try:
        neg_q = False
        if h2:
            if L == K:
                neg_q = False
            else:
                try:
                    if L == K.frac_field(*generators) and len(generators) > 0:
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: There exists a finite set of elements such that L = K(alpha_1, ..., alpha_n)",
    "¬Q: The field extension L/K is not finite"
]

N_HYP = 2
NEG_Q_INDEX = 2