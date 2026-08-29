import sympy
from sympy import Symbol, sympify
from sympy.polys.polytools import is_irreducible

# Top-level setup for potential witness expressions
x = Symbol('x')
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        K = witness.get('K')
        L = witness.get('L')
        alpha = witness.get('alpha')
        f = witness.get('f')
        n = witness.get('n')
    else:
        try:
            K, L, alpha, f, n = witness
        except Exception:
            return [False] * 5 + [False]

    # H1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False

    # H2: L is an extension field of K
    try:
        h2 = bool(L.is_Field and L.unify(K) == L)
    except Exception:
        h2 = False

    # H3: alpha is an element of L
    try:
        val = L.from_sympy(sympify(alpha))
        h3 = val is not None
    except Exception:
        h3 = False

    # H4: f(alpha) = 0
    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else sympify(f)
        free_vars = f_expr.free_symbols
        if len(free_vars) == 1:
            x_var = list(free_vars)[0]
        else:
            x_var = x
        val = f_expr.subs(x_var, alpha).simplify()
        h4 = (val == 0)
    except Exception:
        h4 = False

    # H5: The degree of the field extension K(alpha) over K is exactly n
    try:
        mp = sympy.minpoly(alpha, x, domain=K)
        deg = sympy.degree(mp, x)
        h5 = (deg == n)
    except Exception:
        h5 = False

    # neg_Q: f(x) is not irreducible over K
    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else sympify(f)
        is_irred = is_irreducible(f_expr, domain=K)
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is an extension field of K",
    "H_3: alpha is an element of L",
    "H_4: f(alpha) = 0",
    "H_5: The degree of the field extension K(alpha) over K is exactly n",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 5
NEG_Q_INDEX = 5