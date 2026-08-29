import sympy
from sympy import Symbol
from sympy.polys.domains import QQ, ZZ, GF

# Top-level setup
t = Symbol('t')

def is_perfect(F):
    """
    Checks if a given field F is perfect.
    A field is perfect if its characteristic is 0, or if it is a finite field.
    Rational function fields over finite fields (characteristic p > 0) are not perfect.
    """
    if isinstance(F, str):
        F_str = F.replace(" ", "")
        # Heuristic for string representations like 'GF(2)(t)'
        if "(t)" in F_str and ("GF" in F_str or "F" in F_str):
            return False
        return True
        
    char = getattr(F, 'characteristic', getattr(F, 'char', None))
    if char == 0:
        return True
        
    if getattr(F, 'is_FiniteField', False):
        return True
        
    # Check if it's a fraction field (like GF(p)(t))
    if type(F).__name__ == 'FractionField' or hasattr(F, 'gens'):
        if char is not None and char > 0:
            return False
            
    # If it's a polynomial ring over a finite field (not a field, but for completeness)
    if type(F).__name__ == 'PolynomialRing':
        if char is not None and char > 0:
            return False
            
    return True

def conditions(witness):
    """
    Returns a list of booleans evaluating the remaining hypotheses and the negated conclusion.
    """
    try:
        h1 = bool(is_perfect(witness))
    except Exception:
        h1 = False

    try:
        # The algebraic closure of F is separable over F if and only if F is a perfect field.
        q = bool(is_perfect(witness))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "¬Q: The field extension algebraic_closure(F)/F is not separable"
]

N_HYP = 1
NEG_Q_INDEX = 1