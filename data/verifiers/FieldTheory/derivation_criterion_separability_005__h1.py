import sympy
from sympy import QQ, ZZ, Symbol
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Qx = QQ.frac_field(x)
Qxy = QQ.frac_field(x, y)

def evaluate_extension(witness):
    """
    Evaluates the properties of the field extension L/K.
    Returns a tuple: (is_separable, is_derivation_zero)
    """
    L = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        K, L = witness

    tname = type(L).__name__
    
    # Transcendental extensions (e.g., Q(x)) are separable (in char 0) 
    # but have non-zero derivations (e.g., d/dx).
    if tname == 'FractionField':
        return True, False
        
    # Algebraic extensions over Q are separable and have only the zero derivation.
    if tname == 'AlgebraicField':
        return True, True
        
    # Base fields
    if tname in ['RationalField', 'RealField', 'ComplexField']:
        return True, True
    if L in [sympy.QQ, sympy.RR, sympy.CC]:
        return True, True

    # Heuristics for string-based witnesses
    if isinstance(witness, str):
        s = witness.lower().replace(" ", "")
        # Inseparable extension example: F_p(x) over F_p(x^p)
        if "f_p" in s and "^p" in s:
            return False, False
        # Transcendental extensions
        if "(x)" in s or "(t)" in s or "transcendental" in s:
            return True, False
        # Algebraic extensions
        if "algebraic" in s or "sqrt" in s:
            return True, True
            
    # If the witness is just a symbol like 'x', treat it as the transcendental extension Q(x)
    if isinstance(witness, sympy.Symbol):
        return True, False

    # Fallback: return False for both to avoid false positive counterexamples
    return False, False

def conditions(witness) -> list[bool]:
    try:
        is_sep, is_der_zero = evaluate_extension(witness)
        # The conclusion is: L is separable iff the only derivation is zero.
        # The negated conclusion is True when this equivalence fails.
        neg_q = bool(is_sep != is_der_zero)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence 'L is separable over K iff the only K-derivation is zero' fails"
]

N_HYP = 0
NEG_Q_INDEX = 0