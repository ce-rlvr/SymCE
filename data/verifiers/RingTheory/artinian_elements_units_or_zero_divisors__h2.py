import sympy
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard rings/fields from sympy.
QQ = S.Rationals
ZZ = S.Integers
RR = S.Reals
CC = S.Complexes

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture:
    "In a commutative Artinian ring, every element is either a unit or a zero divisor."
    
    The dropped hypothesis is that the element x must be NONZERO. 
    In any field (which is a commutative Artinian ring), 0 is neither a unit nor a zero divisor.
    
    Expected witness format: a tuple (R, x) where R is the ring and x is the element.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        R, x = witness
    except Exception:
        return [False, False, False, False]

    # Helper to identify fields (which are commutative and Artinian)
    is_field = False
    try:
        if R in (QQ, RR, CC):
            is_field = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            is_field = True
    except Exception:
        pass

    # H_1: R is a commutative ring
    try:
        if is_field or R == ZZ:
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    try:
        if is_field:
            h2 = True
        elif R == ZZ:
            h2 = False
        elif hasattr(R, 'is_artinian'):
            h2 = bool(R.is_artinian)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: x is an element of R
    try:
        if is_field or R == ZZ:
            h3 = bool(x in R)
        elif hasattr(R, '__contains__'):
            h3 = bool(x in R)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: x is neither a unit nor a zero divisor
    try:
        if is_field:
            # In a field, non-zero elements are units, and there are no zero divisors.
            # 0 is neither a unit nor a zero divisor.
            is_u = bool(x != 0 and x in R)
            is_zd = False
        elif R == ZZ:
            is_u = bool(x in (1, -1))
            is_zd = False
        else:
            is_u = bool(R.is_unit(x))
            is_zd = bool(R.is_zero_divisor(x))
            
        neg_q = not (is_u or is_zd)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "H_3: x is an element of R",
    "¬Q: x is neither a unit nor a zero divisor"
]

N_HYP = 3
NEG_Q_INDEX = 3