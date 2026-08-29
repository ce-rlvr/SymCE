import sympy
from sympy import ZZ, QQ, Poly, Symbol
from sympy.abc import x, y, z

# Standard bindings
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The localized ring S^{-1}R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_integral_domain(R):
    if R == ZZ or R == QQ:
        return True
    if hasattr(R, 'is_domain'):
        return bool(R.is_domain)
    if hasattr(R, 'is_IntegralDomain'):
        return bool(R.is_IntegralDomain)
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
        return True
    return False

def is_localized_field(R, S):
    # If S is described as all non-zero elements, the localization is the field of fractions
    if isinstance(S, str):
        s_str = S.lower().replace(" ", "")
        if "0" in s_str and ("\\" in s_str or "-" in s_str or "setminus" in s_str):
            return True
        return False

    if not isinstance(S, (list, set, tuple)):
        S = [S]
        
    # If 0 is in the multiplicative set, the localized ring is the zero ring (not a field)
    for s in S:
        if s == 0 or (hasattr(R, 'zero') and s == R.zero):
            return False
            
    # If R is already a field, localization by any set not containing 0 is a field
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if R == QQ:
        return True
        
    # For standard infinite domains like ZZ or QQ[x], localizing at a finite set 
    # of elements does not yield a field.
    return False

def conditions(witness):
    try:
        # The witness can be a tuple (R, S), a dict, or just the ring R (with S defaulting to {1})
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('r', ZZ))
            S = witness.get('S', witness.get('s', [1]))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            S = [1]
            
        try:
            h1 = is_integral_domain(R)
        except Exception:
            h1 = False
            
        try:
            q = is_localized_field(R, S)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]