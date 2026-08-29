import sympy
from sympy import Symbol, Poly, QQ
from sympy.polys.domains import GF

def conditions(witness) -> list[bool]:
    try:
        F, a, b = witness
    except Exception:
        return [False] * 5

    # H_1: F is a field of characteristic not equal to 2
    try:
        h1 = bool(F.is_Field and F.characteristic != 2)
    except Exception:
        h1 = False

    # H_2: a and b are elements of F
    try:
        _ = F(a)
        _ = F(b)
        h2 = True
    except Exception:
        h2 = False

    # H_3: a is not a square in F
    try:
        Fa = F(a)
        x_sym = Symbol('x')
        c2 = F(1)
        c1 = F(0)
        c0 = -Fa
        poly_a = Poly([c2, c1, c0], x_sym, domain=F)
        h3 = bool(len(poly_a.ground_roots()) == 0)
    except Exception:
        h3 = False

    # H_4: b is not a square in F
    try:
        Fb = F(b)
        x_sym = Symbol('x')
        c2 = F(1)
        c1 = F(0)
        c0 = -Fb
        poly_b = Poly([c2, c1, c0], x_sym, domain=F)
        h4 = bool(len(poly_b.ground_roots()) == 0)
    except Exception:
        h4 = False

    # neg_Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is NOT x^4 - 2(a+b)x^2 + (a-b)^2
    try:
        Fa = F(a)
        Fb = F(b)
        x_sym = Symbol('x')
        p4 = F(1)
        p3 = F(0)
        p2 = F(-2) * (Fa + Fb)
        p1 = F(0)
        p0 = (Fa - Fb)**2
        poly_P = Poly([p4, p3, p2, p1, p0], x_sym, domain=F)
        # If the polynomial is reducible, it cannot be the minimal polynomial.
        neg_q = not bool(poly_P.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: a is not a square in F",
    "H_4: b is not a square in F",
    "¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2"
]

N_HYP = 4
NEG_Q_INDEX = 4