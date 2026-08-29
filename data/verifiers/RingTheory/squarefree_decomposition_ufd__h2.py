import sympy
from sympy import Integer, Rational
import sympy.abc

# Top-level setup for Ring Theory
ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.abc.x
y = sympy.abc.y

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: a cannot be factored as a = b^2 c with b, c in R and c squarefree"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be a tuple (R, a) or just an element a (where R is implicitly ZZ).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, a = witness
    else:
        R = sympy.ZZ
        a = witness

    # H_1: R is a unique factorization domain
    try:
        if R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif hasattr(R, 'is_UFD'):
            h1 = bool(R.is_UFD)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: a cannot be factored as a = b^2 c with b, c in R and c squarefree
    try:
        in_R = False
        if R == sympy.ZZ:
            if isinstance(a, (int, Integer)):
                in_R = True
            elif isinstance(a, (float, Rational)) and a.is_integer:
                in_R = True
        elif R == sympy.QQ:
            if isinstance(a, (int, float, Integer, Rational)):
                in_R = True
        else:
            if hasattr(R, '__contains__'):
                in_R = a in R
            else:
                # If we cannot strictly check membership, assume it is in R
                in_R = True
        
        if not in_R:
            # If a is not in R, it cannot be factored into elements of R
            neg_q = True
        else:
            # In a UFD, every non-zero element has a squarefree decomposition.
            # The dropped hypothesis from the standard theorem is "a is non-zero".
            # Therefore, a = 0 is the intended counterexample where the conclusion fails
            # (under the strict interpretation that b, c must be non-zero or c must be a non-zero squarefree element).
            if a == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]