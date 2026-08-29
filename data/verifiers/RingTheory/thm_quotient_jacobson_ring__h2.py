import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z
from sympy.polys.rings import PolyRing

def is_commutative_jacobson_ring(R):
    """
    Checks if R is a commutative Jacobson ring.
    Fields, ZZ, and their polynomial/quotient rings are Jacobson rings.
    """
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if R in (ZZ, QQ, RR, CC):
        return True
    if isinstance(R, PolyRing):
        return is_commutative_jacobson_ring(R.domain)
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        return is_commutative_jacobson_ring(R.domain)
    if type(R).__name__ == 'QuotientRing':
        base = getattr(R, 'ring', getattr(R, 'base_ring', None))
        if base is not None:
            return is_commutative_jacobson_ring(base)
    return False

def is_ideal(I, R):
    """
    Checks if I is an ideal of R (or represents one, like a generator).
    """
    if I == R:
        return True
    if type(I).__name__ == 'Ideal' and getattr(I, 'ring', None) == R:
        return True
    if R == ZZ and isinstance(I, (int, sympy.Integer)):
        return True
    if isinstance(I, (list, tuple, set)):
        try:
            if hasattr(R, 'ideal'):
                R.ideal(*list(I))
                return True
        except Exception:
            pass
        if R == ZZ and all(isinstance(i, (int, sympy.Integer)) for i in I):
            return True
    try:
        if hasattr(R, 'from_expr'):
            R.from_expr(I)
            return True
    except Exception:
        pass
    try:
        if I in R:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Given a witness (R, I), checks if it is a counterexample to the false conjecture:
    'If R is a commutative Jacobson ring, then the quotient ring R/I is a Jacobson ring.'
    (The dropped hypothesis is that I must be an ideal of R).
    """
    if not isinstance(witness, (tuple, list)) or len(witness) != 2:
        return [False, False]
    
    R, I = witness
    
    try:
        h1 = is_commutative_jacobson_ring(R)
    except Exception:
        h1 = False
        
    try:
        # If I is an ideal of R, R/I is always a Jacobson ring (conclusion holds, neg_Q is False).
        # If I is not an ideal (e.g., a subring or arbitrary subset), R/I is not a valid ring,
        # so it cannot be a Jacobson ring (conclusion fails, neg_Q is True).
        neg_q = not is_ideal(I, R)
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Jacobson ring",
    "¬Q: The quotient ring R/I is not a Jacobson ring"
]

N_HYP = 1
NEG_Q_INDEX = 1