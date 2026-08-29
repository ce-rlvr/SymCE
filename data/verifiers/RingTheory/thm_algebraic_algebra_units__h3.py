import sympy
from sympy import Symbol, QQ, ZZ
from sympy.abc import x, y, t

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (K, A, x) where:
      - K is a SymPy domain representing a field (e.g., QQ)
      - A is a SymPy domain representing a K-algebra (e.g., QQ[t])
      - x is an element of A
    """
    try:
        K, A, elem = witness
    except Exception:
        return [False, False, False, False]

    # H1: K is a field
    try:
        h1 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: A is a unital K-algebra
    try:
        h2 = False
        if getattr(A, 'is_Ring', False):
            # Check if A is an algebra over K (or is K itself)
            if getattr(A, 'domain', None) == K or A == K:
                if hasattr(A, 'one') and A.one is not None:
                    h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of A that is not a zero-divisor
    try:
        h3 = False
        x_A = A(elem)
        if x_A != getattr(A, 'zero', None):
            # In SymPy, standard domains like fields, polynomial rings, and fraction fields
            # are integral domains, meaning non-zero elements are not zero-divisors.
            if getattr(A, 'is_Field', False):
                h3 = True
            elif getattr(A, 'is_PolyRing', False):
                h3 = True
            elif getattr(A, 'is_FracField', False):
                h3 = True
            elif A in (sympy.ZZ, sympy.QQ):
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: x is not a unit in A
    try:
        neg_q = False
        x_A = A(elem)
        is_unit = False
        
        # Try exact division of 1 by x in A
        try:
            q = A.exquo(A.one, x_A)
            if q * x_A == A.one:
                is_unit = True
        except Exception:
            pass
            
        # Fallback checks for unit properties
        if not is_unit and hasattr(A, 'is_unit'):
            if A.is_unit(x_A):
                is_unit = True
                
        if not is_unit and hasattr(x_A, 'is_unit'):
            if x_A.is_unit:
                is_unit = True
                
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: A is a unital K-algebra",
    "H_3: x is an element of A that is not a zero-divisor",
    "¬Q: x is not a unit in A"
]

N_HYP = 3
NEG_Q_INDEX = 3