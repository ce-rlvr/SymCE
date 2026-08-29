import sympy
from sympy import Poly, Symbol
from sympy.abc import x

# Top-level setup for standard domains
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC
GF = sympy.GF

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for Capelli's Irreducibility Theorem (false conjecture).
    Witness should be a tuple: (F, a, n)
    where F is a SymPy domain (e.g., QQ, GF(5)), a is an element of F, and n is an integer.
    """
    try:
        F, a, n = witness
    except Exception:
        return [False] * 5

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: a is a non-zero element of F
    try:
        a_sym = sympy.sympify(a)
        a_F = F.from_sympy(a_sym)
        h2 = bool((a_F is not None) and (a_F != F.zero))
    except Exception:
        h2 = False

    # H_3: n >= 2 is an integer
    try:
        h3 = bool(isinstance(n, int) and n >= 2)
    except Exception:
        h3 = False

    # H_4: If 4 divides n, there is no element c \in F such that a = -4c^4
    try:
        if n % 4 != 0:
            h4 = True
        else:
            x_sym = sympy.Symbol('x')
            a_sym = sympy.sympify(a)
            # 4c^4 + a = 0 <=> a = -4c^4
            p = sympy.Poly(4*x_sym**4 + a_sym, x_sym, domain=F)
            h4 = bool(len(p.ground_roots()) == 0)
    except Exception:
        h4 = False

    # ¬Q: The polynomial x^n - a is reducible over F
    try:
        x_sym = sympy.Symbol('x')
        a_sym = sympy.sympify(a)
        p = sympy.Poly(x_sym**n - a_sym, x_sym, domain=F)
        # is_irreducible returns True if irreducible, False if reducible.
        # We want the negated conclusion (reducible), so it must be False.
        neg_q = (p.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a is a non-zero element of F",
    "H_3: n >= 2 is an integer",
    "H_4: If 4 divides n, there is no element c in F such that a = -4c^4",
    "¬Q: The polynomial x^n - a is reducible over F"
]

N_HYP = 4
NEG_Q_INDEX = 4