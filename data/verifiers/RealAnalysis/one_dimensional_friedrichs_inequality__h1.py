import sympy

# Top-level setup: named object bindings that the witness expression may reference
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, a, b) or a dictionary {'f': f, 'a': a, 'b': b},
    where f is a sympy expression in terms of x (or a callable), and a, b are real numbers.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]

    # H_1: f(a) = 0
    try:
        if callable(f):
            val = f(a)
            f_expr = sympy.sympify(f(x))
        else:
            f_expr = sympy.sympify(f)
            val = f_expr.subs(x, a)
        h1_ok = bool(sympy.simplify(val) == 0)
    except Exception:
        h1_ok = False

    # H_2: a < b
    try:
        h2_ok = bool(a < b)
    except Exception:
        h2_ok = False

    # ¬Q: \int_a^b f(x)^2 dx > \frac{(b-a)^2}{2} \int_a^b f'(x)^2 dx
    try:
        df = sympy.diff(f_expr, x)
        lhs = sympy.integrate(f_expr**2, (x, a, b))
        rhs = sympy.Rational(1, 2) * (b - a)**2 * sympy.integrate(df**2, (x, a, b))
        
        lhs_val = float(sympy.re(lhs.evalf()))
        rhs_val = float(sympy.re(rhs.evalf()))
        
        neg_q_ok = bool(lhs_val - rhs_val > 1e-9)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(a) = 0",
    "H_2: a < b",
    "¬Q: \\int_a^b f(x)^2 dx > \\frac{(b-a)^2}{2} \\int_a^b f'(x)^2 dx"
]

N_HYP = 2
NEG_Q_INDEX = 2