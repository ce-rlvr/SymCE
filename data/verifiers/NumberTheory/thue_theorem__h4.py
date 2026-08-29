import sympy as sp
from sympy.abc import x, y, m

def conditions(witness):
    try:
        if hasattr(witness, 'F'):
            F = witness.F
            m_val = getattr(witness, 'm', sp.Symbol('m'))
        elif isinstance(witness, tuple):
            F = witness[0]
            m_val = witness[1] if len(witness) > 1 else sp.Symbol('m')
        else:
            F = witness
            m_val = sp.Symbol('m')
    except Exception:
        return [False, False, False, False]

    try:
        if not isinstance(F, sp.Expr):
            h1 = False
        else:
            free_vars = F.free_symbols
            if len(free_vars) != 2:
                h1 = False
            else:
                v1, v2 = list(free_vars)
                poly = sp.Poly(F, v1, v2)
                if not poly.is_polynomial:
                    h1 = False
                else:
                    coeffs = poly.coeffs()
                    if not all(sp.sympify(c).is_integer for c in coeffs):
                        h1 = False
                    else:
                        h1 = poly.is_homogeneous
    except Exception:
        h1 = False

    try:
        poly = sp.Poly(F, list(F.free_symbols))
        h2 = poly.total_degree() >= 3
    except Exception:
        h2 = False

    try:
        poly = sp.Poly(F, list(F.free_symbols), domain='QQ')
        h3 = poly.is_irreducible
    except Exception:
        h3 = False

    try:
        # If m is a fixed number, Thue's theorem guarantees finitely many solutions.
        # If m is a free variable, the equation F(x,y) = m has infinitely many solutions (x, y, m).
        if isinstance(m_val, (int, float)) or (isinstance(m_val, sp.Expr) and m_val.is_number):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F(x,y) is a homogeneous polynomial in two variables with integer coefficients",
    "H_2: the degree of F is at least 3",
    "H_3: F(x,y) is irreducible over the field of rational numbers",
    "¬Q: The Diophantine equation F(x,y) = m has infinitely many solutions in integers"
]

N_HYP = 3
NEG_Q_INDEX = 3