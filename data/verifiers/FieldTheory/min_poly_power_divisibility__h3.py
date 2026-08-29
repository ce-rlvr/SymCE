import sympy
from sympy import Symbol, Poly, minpoly, rem

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary providing (F, alpha, n, p, q) or a tuple.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            alpha = witness.get('alpha')
            n = witness.get('n')
            p = witness.get('p')
            q = witness.get('q')
        else:
            F, alpha, n, p, q = witness
    except Exception:
        return [False] * 5

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: alpha is an algebraic element over F
    try:
        mp_alpha = minpoly(alpha, x, domain=F)
        h2 = mp_alpha is not None
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    try:
        h3 = isinstance(n, int) and n > 0
    except Exception:
        h3 = False

    # H_4: q(x) is the minimal polynomial of alpha^n over F
    try:
        mp_alphan = minpoly(alpha**n, x, domain=F)
        q_expr = q.as_expr() if hasattr(q, 'as_expr') else q
        q_poly = Poly(q_expr, x, domain=F)
        mp_poly = Poly(mp_alphan, x, domain=F)
        h4 = q_poly.monic() == mp_poly.monic()
    except Exception:
        h4 = False

    # ¬Q: p(x) does not divide q(x^n) over F
    try:
        q_expr = q.as_expr() if hasattr(q, 'as_expr') else q
        p_expr = p.as_expr() if hasattr(p, 'as_expr') else p
        q_xn = q_expr.subs(x, x**n)
        remainder = rem(q_xn, p_expr, x, domain=F)
        neg_q = not Poly(remainder, x, domain=F).is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: n is a positive integer",
    "H_4: q(x) is the minimal polynomial of alpha^n over F",
    "¬Q: p(x) does not divide q(x^n) over F"
]

N_HYP = 4
NEG_Q_INDEX = 4