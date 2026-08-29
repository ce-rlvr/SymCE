import sympy
from sympy import Symbol, QQ, GF
from sympy.polys.polytools import factor_list

# Top-level setup for the namespace
x = Symbol('x')

def conditions(witness):
    """
    Checks the witness against the hypotheses and negated conclusion.
    The witness can be a tuple (F, a, b) or just (a, b) where F defaults to QQ.
    """
    try:
        if len(witness) == 2:
            F = QQ
            a, b = witness
        elif len(witness) == 3:
            F, a, b = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: F is a field of characteristic not equal to 2
    try:
        char = getattr(F, 'char', getattr(F, 'characteristic', None))
        h1 = getattr(F, 'is_Field', False) and char != 2
    except Exception:
        h1 = False

    # H_2: a and b are elements of F
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        # Verify that a and b can be converted to elements of the domain F
        F.from_sympy(a_sym)
        F.from_sympy(b_sym)
        h2 = True
    except Exception:
        h2 = False

    # H_3: b is not a square in F
    # Equivalent to x^2 - b being irreducible over F
    try:
        poly_b = x**2 - b_sym
        factors_b = factor_list(poly_b, domain=F)
        # Irreducible iff there is exactly 1 factor and its multiplicity is 1
        h3 = len(factors_b[1]) == 1 and factors_b[1][0][1] == 1
    except Exception:
        h3 = False

    # H_4: ab is not a square in F
    # Equivalent to x^2 - ab being irreducible over F
    try:
        poly_ab = x**2 - a_sym * b_sym
        factors_ab = factor_list(poly_ab, domain=F)
        h4 = len(factors_ab[1]) == 1 and factors_ab[1][0][1] == 1
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is NOT x^4 - 2(a+b)x^2 + (a-b)^2
    # Since sqrt(a) + sqrt(b) is always a root of this polynomial, it is the minimal polynomial
    # if and only if it is irreducible over F. Thus, the conclusion fails (¬Q is True) 
    # if and only if the polynomial is reducible over F.
    try:
        poly_q = x**4 - 2*(a_sym + b_sym)*x**2 + (a_sym - b_sym)**2
        factors_q = factor_list(poly_q, domain=F)
        # Reducible if there is more than 1 factor, or 1 factor with multiplicity > 1
        neg_q = not (len(factors_q[1]) == 1 and factors_q[1][0][1] == 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: b is not a square in F",
    "H_4: ab is not a square in F",
    "¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2"
]

N_HYP = 4
NEG_Q_INDEX = 4