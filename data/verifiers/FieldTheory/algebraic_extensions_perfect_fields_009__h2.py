import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')
QQ = sympy.QQ
ZZ = sympy.ZZ

def is_perfect_field(F):
    """
    Checks if a given SymPy domain represents a perfect field.
    A field is perfect if it has characteristic 0, or if it has characteristic p > 0
    and every element is a p-th power (e.g., finite fields).
    """
    if not getattr(F, 'is_Field', False):
        return False
    
    char = getattr(F, 'characteristic', None)
    if char == 0:
        return True
    
    if char is not None and char > 0:
        name = type(F).__name__
        # Finite fields are perfect
        if 'FiniteField' in name or 'GaloisField' in name or name == 'FF':
            return True
        # Rational function fields over finite fields are imperfect
        if 'FractionField' in name:
            return False
        # Fallback check for other finite fields
        if hasattr(F, 'order'):
            try:
                order = F.order() if callable(F.order) else F.order
                if order < float('inf'):
                    return True
            except Exception:
                pass
                
    return False

def conditions(witness) -> list[bool]:
    # The witness can be a tuple (K, L) or just L (where K is inferred as L's base domain)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
        else:
            L = witness
            if hasattr(L, 'domain'):
                K = L.domain
            else:
                K = None
    except Exception:
        return [False, False]

    # H_1: K is a perfect field
    try:
        h1 = bool(is_perfect_field(K))
    except Exception:
        h1 = False

    # ¬Q: L is NOT a perfect field (but it must be a field)
    try:
        is_L_field = getattr(L, 'is_Field', False)
        neg_q = bool(is_L_field and not is_perfect_field(L))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a perfect field",
    "¬Q: L is not a perfect field"
]

N_HYP = 1
NEG_Q_INDEX = 1