import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Check the witness against the remaining hypotheses and the negated conclusion.
    The witness can be a tuple (R, a, b, n) or (a, b, n) where R is implicitly ZZ.
    """
    try:
        if len(witness) == 4:
            R, a, b, n = witness
        elif len(witness) == 3:
            a, b, n = witness
            R = ZZ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    # H_2: a and b are elements of R
    try:
        h2 = (a in R) and (b in R)
    except Exception:
        h2 = False
        
    # H_3: n is a positive integer
    try:
        h3 = (type(n) is int or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h3 = False
        
    # ¬Q: a does not divide b in R
    try:
        if a == getattr(R, 'zero', 0) or a == 0:
            divides = (b == getattr(R, 'zero', 0) or b == 0)
        else:
            try:
                # exquo computes the exact quotient in the domain R.
                # It raises an exception (e.g., ExactQuotientFailed) if a does not divide b.
                R.exquo(b, a)
                divides = True
            except Exception:
                divides = False
        neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a and b are elements of R",
    "H_3: n is a positive integer",
    "¬Q: a does not divide b in R"
]

N_HYP = 3
NEG_Q_INDEX = 3