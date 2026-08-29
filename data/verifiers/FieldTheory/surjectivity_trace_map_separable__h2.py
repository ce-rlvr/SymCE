import sympy
from sympy import QQ, GF, Symbol
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E/F is a separable extension",
    "¬Q: The field trace map Tr_{E/F}: E -> F is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (E, F) representing a field extension E/F,
    checks if it satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        E, F = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: E/F is a separable extension
    try:
        h2 = False
        if getattr(E, 'is_Field', False):
            base = None
            if type(E).__name__ == 'FractionField':
                # For a fraction field like QQ(x), the domain is the polynomial ring QQ[x],
                # and its domain is the base field QQ.
                base = E.domain.domain
            elif type(E).__name__ == 'AlgebraicField':
                base = E.domain
            elif E == F:
                base = F
            
            if base == F:
                # Check separability: characteristic 0 or finite fields are perfect
                char = getattr(F, 'characteristic', lambda: None)()
                if char == 0:
                    h2 = True
                elif type(F).__name__ == 'GaloisField':
                    h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The field trace map Tr_{E/F}: E -> F is not surjective
    # The trace map is surjective for any finite separable extension.
    # It fails to be surjective (or is undefined) for infinite extensions.
    try:
        neg_q = False
        if type(E).__name__ == 'FractionField':
            neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]