import sympy
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a unique factorization domain
    # We accept integers and SymPy expressions (like polynomials) as elements of a UFD.
    try:
        h1 = all(isinstance(val, (int, sympy.Integer, sympy.Expr)) for val in (a, b, c))
    except Exception:
        h1 = False
        
    # H_2: a, b, c are non-zero elements of R
    try:
        h2 = all(val != 0 for val in (a, b, c))
    except Exception:
        h2 = False
        
    # neg_Q: lcm(a, c) does not divide lcm(b, c)
    try:
        l1 = sympy.lcm(a, c)
        l2 = sympy.lcm(b, c)
        
        # Check if l1 divides l2 in the ring
        ratio = sympy.cancel(sympy.S(l2) / sympy.S(l1))
        divides = (ratio.as_numer_denom()[1] == 1)
        
        neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "¬Q: lcm(a, c) does not divide lcm(b, c)"
]

N_HYP = 2
NEG_Q_INDEX = 2