import sympy
from sympy import I, pi, exp, Abs, simplify
from sympy.abc import x, y, z

# Top-level setup
# No special named objects needed for this field theory conjecture,
# but standard symbols x, y, z are available.

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # Extract witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            # Witness could be (n, Phi, alpha) or (Phi, n, alpha)
            if isinstance(witness[0], (int, sympy.Integer)):
                n, Phi, alpha = witness
            else:
                Phi, n, alpha = witness
        elif len(witness) == 2:
            # Witness could be just (n, alpha)
            n, alpha = witness
            Phi = None
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    var = sympy.Symbol('x')

    # H1: Let Phi_n(x) be the n-th cyclotomic polynomial over Q
    try:
        n_val = int(n)
        expected_Phi = sympy.polys.specialpolys.cyclotomic_poly(n_val, var)
        if Phi is not None:
            if hasattr(Phi, 'as_expr'):
                Phi_expr = Phi.as_expr()
            else:
                Phi_expr = Phi
            free_vars = Phi_expr.free_symbols
            v = list(free_vars)[0] if free_vars else var
            expected_Phi_v = sympy.polys.specialpolys.cyclotomic_poly(n_val, v)
            h1 = bool(simplify(Phi_expr - expected_Phi_v) == 0)
            Phi = Phi_expr
        else:
            Phi = expected_Phi
            h1 = True
    except Exception:
        h1 = False

    # H2: Let alpha in C be a root of Phi_n(x)
    try:
        if h1 and Phi is not None:
            free_vars = Phi.free_symbols
            v = list(free_vars)[0] if free_vars else var
            val = simplify(Phi.subs(v, alpha))
            if val == 0:
                h2 = True
            else:
                # Fallback to numerical evaluation for complex algebraic roots
                try:
                    h2 = abs(complex(val.evalf())) < 1e-9
                except Exception:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The absolute value (modulus) of alpha is exactly 1 (must FAIL)
    try:
        abs_val = simplify(Abs(alpha))
        if abs_val == 1:
            neg_q = False
        else:
            # Fallback to numerical evaluation
            try:
                num_abs = abs(complex(sympy.N(alpha)))
                neg_q = abs(num_abs - 1.0) > 1e-9
            except Exception:
                neg_q = bool(abs_val != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial over Q",
    "H_2: alpha is a root of Phi_n(x)",
    "¬Q: The absolute value of alpha is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2