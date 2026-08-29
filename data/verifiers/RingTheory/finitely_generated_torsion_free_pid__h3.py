import sympy
from sympy import ZZ, QQ
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A finitely generated module over a PID is free."
    
    The witness is expected to be a tuple: (domain, inv_factors)
    where `domain` is a SymPy domain (e.g., ZZ) representing the PID R,
    and `inv_factors` is a list of elements in R representing the invariant 
    factors of the finitely generated R-module M.
    """
    try:
        domain, inv_factors = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(domain.is_PID)
    except Exception:
        h1 = False
        
    # H_2: M is a finitely generated R-module
    try:
        h2 = isinstance(inv_factors, (list, tuple)) and all(d in domain for d in inv_factors)
    except Exception:
        h2 = False
        
    # ¬Q: M is not a free R-module
    # M is free iff all its invariant factors are either 0 or units in R.
    try:
        is_free = True
        for d in inv_factors:
            if d == domain.zero:
                continue
            
            try:
                if hasattr(domain, 'is_unit'):
                    is_unit = bool(domain.is_unit(d))
                else:
                    # If 1 can be exactly divided by d, then d is a unit.
                    domain.exquo(domain.one, d)
                    is_unit = True
            except Exception:
                is_unit = False
            
            if not is_unit:
                is_free = False
                break
                
        neg_q = not is_free
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2