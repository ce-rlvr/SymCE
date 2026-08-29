import sympy
from sympy import Symbol, QQ
from sympy.polys.polytools import factor_list

def is_square(val, K):
    if K == QQ:
        try:
            return sympy.sqrt(val) in K
        except Exception:
            return False
            
    try:
        # For finite fields of odd characteristic, use Euler's criterion
        if getattr(K, 'is_FiniteField', False):
            q = getattr(K, 'order', getattr(K, 'size', None))
            if q is not None:
                v = K(val)
                if v == K(0):
                    return True
                return v**((q - 1) // 2) == K(1)
    except Exception:
        pass
        
    try:
        return sympy.sqrt(val) in K
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness can be a tuple (K, a, b) or just (a, b) in which case K is assumed to be QQ.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                K = QQ
                a, b = witness
            elif len(witness) == 3:
                K, a, b = witness
            else:
                return [False] * 4 + [False]
        else:
            return [False] * 4 + [False]
    except Exception:
        return [False] * 4 + [False]

    # H_1: K is a field of characteristic not equal to 2
    try:
        if hasattr(K, 'characteristic'):
            char = K.characteristic()
        elif hasattr(K, 'char'):
            char = K.char
        else:
            char = None
            
        h1 = getattr(K, 'is_Field', False) and (char is not None) and (char != 2)
    except Exception:
        h1 = False

    # H_2: a and b are elements of K
    try:
        h2 = (a in K) and (b in K)
    except Exception:
        h2 = False

    # H_3: b is not a square in K
    try:
        h3 = not is_square(b, K)
    except Exception:
        h3 = False

    # H_4: a^2 - 4b is not a square in K
    try:
        val = a**2 - 4*b
        h4 = not is_square(val, K)
    except Exception:
        h4 = False

    # ¬Q: The polynomial x^4 + a x^2 + b is reducible over K
    try:
        x = Symbol('x')
        poly = x**4 + a*x**2 + b
        factors = factor_list(poly, domain=K)[1]
        # factor_list returns (constant, [(factor1, exp1), (factor2, exp2), ...])
        # The polynomial is reducible if the sum of the exponents of its irreducible factors > 1
        num_factors = sum(exp for f, exp in factors)
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: a and b are elements of K",
    "H_3: b is not a square in K",
    "H_4: a^2 - 4b is not a square in K",
    "¬Q: The polynomial x^4 + a x^2 + b is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4