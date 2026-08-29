import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    # witness can be (f, a, b, theta, mu, E) or (f, a, b, theta, E)
    try:
        if len(witness) == 6:
            f, a, b, theta, mu, E = witness
            a_f = float(a)
            b_f = float(b)
        elif len(witness) == 5:
            f, a, b, theta, E = witness
            a_f = float(a)
            b_f = float(b)
            # Compute mu if not provided
            if isinstance(f, sympy.Expr):
                expected_mu_expr = sympy.integrate(f, (x, a, b))
                if expected_mu_expr.has(sympy.Integral):
                    f_lam = sympy.lambdify(x, f, 'math')
                    mu = sum(f_lam(a_f + (b_f - a_f) * (i + 0.5) / 1000.0) for i in range(1000)) / 1000.0
                else:
                    mu = float(expected_mu_expr) / (b_f - a_f)
            elif callable(f):
                mu = sum(f(a_f + (b_f - a_f) * (i + 0.5) / 1000.0) for i in range(1000)) / 1000.0
            else:
                mu = float(f)
        else:
            return [False] * 4 + [False]
    except Exception:
        return [False] * 4 + [False]

    # H1: f is a non-negative, continuous real-valued function on the interval a to b that is not identically zero
    h1 = False
    try:
        if a_f < b_f:
            pts = [a_f + (b_f - a_f) * i / 100.0 for i in range(101)]
            if isinstance(f, sympy.Expr):
                f_lam = sympy.lambdify(x, f, 'math')
                vals = [float(f_lam(p)) for p in pts]
            elif callable(f):
                vals = [float(f(p)) for p in pts]
            else:
                vals = [float(f) for p in pts]
            
            if not any(v < -1e-7 for v in vals) and not all(abs(v) < 1e-7 for v in vals):
                h1 = True
    except Exception:
        h1 = False

    # H2: 0 < theta < 1
    h2 = False
    try:
        if 0 < float(theta) < 1:
            h2 = True
    except Exception:
        h2 = False

    # H3: mu = 1/(b-a) \int_a^b f(x) dx
    h3 = False
    try:
        if isinstance(f, sympy.Expr):
            expected_mu_expr = sympy.integrate(f, (x, a, b))
            if expected_mu_expr.has(sympy.Integral):
                f_lam = sympy.lambdify(x, f, 'math')
                expected_mu = sum(f_lam(a_f + (b_f - a_f) * (i + 0.5) / 1000.0) for i in range(1000)) / 1000.0
            else:
                expected_mu = float(expected_mu_expr) / (b_f - a_f)
        elif callable(f):
            expected_mu = sum(f(a_f + (b_f - a_f) * (i + 0.5) / 1000.0) for i in range(1000)) / 1000.0
        else:
            expected_mu = float(f)
            
        if abs(float(mu) - float(expected_mu)) < 1e-4:
            h3 = True
    except Exception:
        h3 = False

    # H4: |E| denotes the Lebesgue measure of the set E
    h4 = False
    meas_E = 0.0
    try:
        if hasattr(E, 'measure'):
            meas_E = float(E.measure)
            h4 = True
        elif isinstance(E, (list, tuple)):
            meas_E = sum(float(d - c) for c, d in E)
            h4 = True
        elif isinstance(E, (int, float)):
            meas_E = float(E)
            h4 = True
    except Exception:
        h4 = False

    # neg_Q: |E| < (b-a) (1-theta)^2 mu^2 / (1/(b-a) \int_a^b f(x)^2 dx)
    neg_q = False
    try:
        if isinstance(f, sympy.Expr):
            int_f2_expr = sympy.integrate(f**2, (x, a, b))
            if int_f2_expr.has(sympy.Integral):
                f_lam = sympy.lambdify(x, f, 'math')
                int_f2 = sum(f_lam(a_f + (b_f - a_f) * (i + 0.5) / 1000.0)**2 for i in range(1000)) * (b_f - a_f) / 1000.0
            else:
                int_f2 = float(int_f2_expr)
        elif callable(f):
            int_f2 = sum(f(a_f + (b_f - a_f) * (i + 0.5) / 1000.0)**2 for i in range(1000)) * (b_f - a_f) / 1000.0
        else:
            int_f2 = float(f)**2 * (b_f - a_f)
            
        denom = float(int_f2) / (b_f - a_f)
        if denom > 1e-12:
            rhs = (b_f - a_f) * (1 - float(theta))**2 * float(mu)**2 / denom
            if meas_E < rhs - 1e-9:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-negative, continuous real-valued function on the interval a to b that is not identically zero",
    "H_2: 0 < theta < 1",
    "H_3: mu = 1/(b-a) int_a^b f(x) dx",
    "H_4: |E| denotes the Lebesgue measure of the set E",
    "not Q: |E| < (b-a) (1-theta)^2 mu^2 / (1/(b-a) int_a^b f(x)^2 dx)"
]

N_HYP = 4
NEG_Q_INDEX = 4