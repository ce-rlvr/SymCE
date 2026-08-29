import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z
from sympy.polys.domains import GF

# Setup standard objects that might be used in witnesses
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)

def is_algebraic_over_prime(E):
    """Check if a field is algebraic over its prime subfield."""
    if E == QQ:
        return True
    try:
        if getattr(E, 'is_FiniteField', False):
            return True
    except Exception:
        pass
    try:
        if getattr(E, 'is_AlgebraicField', False):
            return is_algebraic_over_prime(E.domain)
    except Exception:
        pass
    return False

def is_subfield(F, E):
    """Check if F is a subfield of E."""
    if F == E:
        return True
    try:
        # SymPy domains can often be unified to the larger domain if one is a subring
        if F.unify(E) == E:
            return True
    except Exception:
        pass
    
    try:
        if getattr(E, 'domain', None) is not None:
            if is_subfield(F, E.domain):
                return True
    except Exception:
        pass

    try:
        # QQ is a subfield of any field of characteristic 0
        if F == QQ and getattr(E, 'char', None) == 0:
            return True
    except Exception:
        pass

    return False

def is_algebraic_over(E, F):
    """Check if field E is an algebraic extension of field F."""
    if E == F:
        return True
    
    # If E is algebraic over its prime subfield, it's algebraic over any subfield F
    if is_algebraic_over_prime(E) and is_subfield(F, E):
        return True

    try:
        if getattr(E, 'is_AlgebraicField', False):
            return is_algebraic_over(E.domain, F)
    except Exception:
        pass
    
    try:
        if getattr(E, 'is_FractionField', False) or getattr(E, 'is_PolynomialRing', False):
            return False
    except Exception:
        pass

    return False

def is_separable_over(E, F):
    """Check if field E is a separable extension of field F."""
    if not is_algebraic_over(E, F):
        return False
    try:
        if getattr(F, 'char', None) == 0:
            return True
    except Exception:
        pass
    try:
        if getattr(F, 'has_CharacteristicZero', False):
            return True
    except Exception:
        pass
    try:
        if getattr(F, 'is_FiniteField', False):
            return True
    except Exception:
        pass
    if F == QQ:
        return True
    return False

def conditions(witness):
    """
    Check the hypotheses and negated conclusion for the false conjecture:
    'If F <= E <= K are fields and E/F is separable algebraic, then K/F is separable algebraic.'
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        F, E, K = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F, E, and K are fields such that F is a subfield of E, and E is a subfield of K
    try:
        h1 = (getattr(F, 'is_Field', False) and 
              getattr(E, 'is_Field', False) and 
              getattr(K, 'is_Field', False) and 
              is_subfield(F, E) and 
              is_subfield(E, K))
    except Exception:
        h1 = False

    # H_2: Every element of E is algebraic and separable over F
    try:
        h2 = is_algebraic_over(E, F) and is_separable_over(E, F)
    except Exception:
        h2 = False

    # ¬Q: K is not an algebraic and separable extension of F
    try:
        q = is_algebraic_over(K, F) and is_separable_over(K, F)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F, E, and K are fields such that F is a subfield of E, and E is a subfield of K",
    "H_2: Every element of E is algebraic and separable over F",
    "¬Q: K is not an algebraic and separable extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2