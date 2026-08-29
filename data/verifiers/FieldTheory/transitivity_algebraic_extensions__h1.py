import sympy
from sympy import QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z

def to_domain(obj):
    """
    Helper to convert a list of generators into a SymPy field domain.
    If the object is already a field domain, it is returned as is.
    """
    if getattr(obj, 'is_Field', False):
        return obj
    if isinstance(obj, (list, tuple)):
        if len(obj) == 0:
            return QQ
        try:
            # Try to create an algebraic extension over QQ
            return QQ.algebraic_field(*obj)
        except Exception:
            try:
                # Fallback to a transcendental extension (fraction field)
                return QQ.frac_field(*obj)
            except Exception:
                pass
    return obj

def is_algebraic_extension(E, F):
    """
    Checks if the SymPy domain E is an algebraic field extension of F.
    """
    try:
        # Both must be fields
        if not (getattr(E, 'is_Field', False) and getattr(F, 'is_Field', False)):
            return False
        
        # Trivial extension
        if E == F:
            return True
            
        # Special case for ComplexField over RealField
        if E.__class__.__name__ == 'ComplexField' and F.__class__.__name__ == 'RealField':
            return True
            
        # F must be a subfield of E. We check this by unifying.
        try:
            if E.unify(F) != E:
                return False
        except Exception:
            return False
            
        # Traverse the domain hierarchy of E to see if it's algebraic over F
        current = E
        while current is not None:
            if current == F:
                return True
            
            if current.__class__.__name__ == 'AlgebraicField':
                # Move down to the base field of this algebraic extension
                current = current.domain
            else:
                # If we hit a non-algebraic domain, check if F is a superfield of it.
                # If F contains this base domain, then E is algebraic over F.
                try:
                    if F.unify(current) == F:
                        return True
                except Exception:
                    pass
                return False
                
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    "If L/K is algebraic and M/L is algebraic, then M/K is algebraic."
    
    The witness should be a tuple of three SymPy domains (K, L, M).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        K_raw, L_raw, M_raw = witness
    except Exception:
        return [False, False, False]
        
    try:
        K = to_domain(K_raw)
        L = to_domain(L_raw)
        M = to_domain(M_raw)
    except Exception:
        K, L, M = K_raw, L_raw, M_raw

    # H_1: The field extension L/K is algebraic
    try:
        h1_ok = is_algebraic_extension(L, K)
    except Exception:
        h1_ok = False

    # H_2: The field extension M/L is algebraic
    try:
        h2_ok = is_algebraic_extension(M, L)
    except Exception:
        h2_ok = False

    # ¬Q: The field extension M/K is NOT algebraic
    try:
        neg_q_ok = not is_algebraic_extension(M, K)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: The field extension L/K is algebraic",
    "H_2: The field extension M/L is algebraic",
    "¬Q: The field extension M/K is not algebraic"
]

N_HYP = 2
NEG_Q_INDEX = 2