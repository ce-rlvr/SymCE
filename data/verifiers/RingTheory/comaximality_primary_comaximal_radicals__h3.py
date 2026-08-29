import sympy
from sympy import factorint, gcd, degree
from sympy.polys.polytools import factor_list
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z')
Z = sympy.S.Integers
Q = sympy.S.Rationals

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q_1 and Q_2 are primary ideals of R",
    "¬Q: Q_1 and Q_2 are not comaximal (Q_1 + Q_2 != R)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(witness):
    """Extracts the two ideal generators from the witness."""
    if isinstance(witness, dict):
        if 'Q1' in witness and 'Q2' in witness:
            a, b = witness['Q1'], witness['Q2']
        elif 'q1' in witness and 'q2' in witness:
            a, b = witness['q1'], witness['q2']
        else:
            vals = list(witness.values())
            if len(vals) >= 2:
                a, b = vals[-2], vals[-1]
            else:
                return None, None
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            a, b = witness
        elif len(witness) == 3:
            _, a, b = witness
        else:
            return None, None
    else:
        return None, None
        
    # Unwrap single-element lists/tuples/sets often used to denote ideals
    if isinstance(a, (list, tuple)) and len(a) == 1:
        a = a[0]
    if isinstance(b, (list, tuple)) and len(b) == 1:
        b = b[0]
        
    if isinstance(a, set) and len(a) == 1:
        a = list(a)[0]
    if isinstance(b, set) and len(b) == 1:
        b = list(b)[0]
        
    return a, b

def is_primary(q):
    """Checks if the principal ideal (q) is primary in Z or a polynomial ring over a field."""
    # Try integer (Z)
    try:
        val = int(q)
        val = abs(val)
        if val == 0:
            return True
        if val == 1:
            return False
        return len(factorint(val)) == 1
    except Exception:
        pass
        
    # Try polynomial
    try:
        if q == 0:
            return True
        factors = factor_list(q)
        if len(factors[1]) == 1:
            return True
        return False
    except Exception:
        return False

def is_comaximal(a, b):
    """Checks if the principal ideals (a) and (b) are comaximal."""
    # Try integer (Z)
    try:
        val_a = int(a)
        val_b = int(b)
        return math.gcd(val_a, val_b) == 1
    except Exception:
        pass
        
    # Try polynomial
    try:
        g = gcd(a, b)
        if g == 0:
            return False
        return g.is_number or g == 1 or g == -1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    a, b = get_elements(witness)
    if a is None or b is None:
        return [False, False, False]
        
    # H_1: R is a commutative ring
    # We implicitly work in Z or a polynomial ring over a field, which are commutative.
    h1 = True
    
    # H_2: Q_1 and Q_2 are primary ideals of R
    try:
        h2 = bool(is_primary(a) and is_primary(b))
    except Exception:
        h2 = False
        
    # ¬Q: Q_1 and Q_2 are NOT comaximal (Q_1 + Q_2 != R)
    try:
        neg_q = not bool(is_comaximal(a, b))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]