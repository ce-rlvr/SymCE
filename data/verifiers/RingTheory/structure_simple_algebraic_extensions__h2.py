import sympy
from sympy import Symbol, Poly, zeros, eye, Matrix

# Top-level setup
x = Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Parse witness: can be a dict or a tuple (alpha, m_expr, [x_sym])
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            m_expr = witness.get('m')
            x_sym = witness.get('x', x)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                alpha, m_expr, x_sym = witness
            elif len(witness) == 2:
                alpha, m_expr = witness
                x_sym = x
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        if isinstance(m_expr, Poly):
            p = m_expr
            if x_sym is None:
                x_sym = p.gens[0]
        else:
            if x_sym is None:
                free = m_expr.free_symbols
                x_sym = list(free)[0] if free else x
            p = Poly(m_expr, x_sym)
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    # We implicitly assume F is the field of fractions of the matrix entries (e.g., QQ).
    # We just verify that alpha is a valid matrix-like object.
    try:
        h1_ok = hasattr(alpha, 'shape')
    except Exception:
        h1_ok = False

    # H2: alpha is an element of E that is algebraic over F
    # Any square matrix over a field is algebraic over that field.
    try:
        h2_ok = hasattr(alpha, 'is_square') and alpha.is_square
    except Exception:
        h2_ok = False

    # H3: m(x) is the minimal polynomial of alpha over F
    try:
        def eval_poly(poly, mat):
            coeffs = poly.all_coeffs()
            deg = poly.degree()
            n = mat.shape[0]
            res = zeros(n, n)
            for i, c in enumerate(coeffs):
                if deg - i == 0:
                    res += c * eye(n)
                else:
                    res += c * (mat ** (deg - i))
            return res

        if p.LC() != 1:
            h3_ok = False
        elif eval_poly(p, alpha) != zeros(alpha.shape[0], alpha.shape[0]):
            h3_ok = False
        else:
            h3_ok = True
            # Check that no proper divisor of p annihilates alpha.
            # It is sufficient to check p / f for all irreducible factors f of p.
            factors = sympy.factor_list(p)[1]
            for f_poly, _ in factors:
                q = p.quo(f_poly)
                if eval_poly(q, alpha) == zeros(alpha.shape[0], alpha.shape[0]):
                    h3_ok = False
                    break
    except Exception:
        h3_ok = False

    # neg_Q: The field extension F(alpha) is isomorphic to the quotient ring F[x]/(m(x))
    # The conclusion implies F[x]/(m(x)) is a field. It fails if m(x) is NOT irreducible.
    try:
        neg_q = not p.is_irreducible
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an element of E that is algebraic over F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "¬Q: The field extension F(alpha) is NOT isomorphic to the quotient ring of polynomials modulo m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3