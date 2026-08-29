import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)
n = sympy.Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    a_n = None
    R = None
    f = None
    
    # Unpack the witness
    if isinstance(witness, dict):
        a_n = witness.get('a_n')
        R = witness.get('R')
        f = witness.get('f')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            a_n, R, f = witness
        elif len(witness) == 2:
            a_n, R = witness
    else:
        f = witness

    if callable(f):
        try:
            f = f(x)
        except Exception:
            pass

    # H_1: 0 < R < oo
    h1 = False
    try:
        if R is None and a_n is not None:
            a_n_expr = a_n(n) if callable(a_n) else a_n
            a_n_expr = sympy.sympify(a_n_expr)
            ratio = sympy.limit(sympy.Abs(a_n_expr / a_n_expr.subs(n, n+1)), n, sympy.oo)
            if ratio != sympy.oo and ratio != 0 and not ratio.has(sympy.nan):
                R = ratio
                
        if R is not None:
            R_val = float(R)
            if 0 < R_val < float('inf'):
                h1 = True
    except Exception:
        h1 = False

    # H_2: a_n >= 0 for all n >= 0
    h2 = False
    try:
        if a_n is not None:
            h2 = True
            for i in range(20):
                if callable(a_n):
                    val = a_n(i)
                elif isinstance(a_n, (list, tuple)):
                    val = a_n[i] if i < len(a_n) else 0
                else:
                    val = sympy.sympify(a_n).subs(n, i)
                
                val = sympy.sympify(val)
                if val.is_real is False or val < 0:
                    h2 = False
                    break
        elif f is not None:
            h2 = True
            series = sympy.series(f, x, 0, 20).removeO()
            for i in range(20):
                coeff = series.coeff(x, i)
                if coeff.is_real is False or coeff < 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The sum function f(x) does NOT have a singularity at x = R
    # (meaning it can be analytically continued to a neighborhood of R)
    neg_q = False
    try:
        if f is None and a_n is not None:
            a_n_expr = a_n(n) if callable(a_n) else a_n
            f_sum = sympy.Sum(sympy.sympify(a_n_expr) * x**n, (n, 0, sympy.oo)).doit()
            if not isinstance(f_sum, sympy.Sum):
                f = f_sum

        if f is not None and R is not None:
            is_analytic = True
            for i in range(6):
                deriv = sympy.diff(f, x, i)
                val = deriv.subs(x, R)
                if val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
                    is_analytic = False
                    break
                if val.is_real is False:
                    is_analytic = False
                    break
            neg_q = is_analytic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The radius of convergence satisfies 0 < R < infinity",
    "H_2: a_n >= 0 for all n >= 0",
    "¬Q: The sum function f(x) does not have a singularity at x = R"
]

N_HYP = 2
NEG_Q_INDEX = 2