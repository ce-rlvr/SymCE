import sympy
from sympy import Symbol, Abs, integrate, limit, oo, Integral, sympify
from sympy.abc import x, n

CONDITION_LABELS = [
    "H_1: interval is bounded and closed in R",
    "H_2: f_n is a sequence of Riemann integrable functions",
    "H_3: p >= 1 is a real number",
    "¬Q: f_n does not converge to f in L^p-norm"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    'Uniform Convergence implies L^p Convergence on Bounded Intervals'
    (where the uniform convergence hypothesis was dropped).
    
    Expected witness structure:
    A tuple (a, b, f_n, f, p) or a dictionary with these keys, where:
      - a, b: bounds of the interval
      - f_n: sympy expression for the sequence of functions (using symbols x and n)
      - f: sympy expression for the limit function (using symbol x)
      - p: real number >= 1
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            f_n = witness['f_n']
            f = witness['f']
            p = witness['p']
        else:
            a, b, f_n, f, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: interval is bounded and closed in R
    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        h1 = bool(a_sym.is_real and b_sym.is_real and a_sym < b_sym)
    except Exception:
        h1 = False

    # H_2: f_n is a sequence of Riemann integrable functions
    try:
        h2 = True
        for test_n in [1, 2]:
            fn_sub = sympify(f_n).subs(n, test_n)
            val = integrate(fn_sub, (x, a_sym, b_sym))
            if val.has(Integral) or not val.is_finite:
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: p >= 1 is a real number
    try:
        p_sym = sympify(p)
        h3 = bool(p_sym.is_real and p_sym >= 1)
    except Exception:
        h3 = False

    # ¬Q: f_n does not converge to f in L^p-norm
    neg_q = False
    try:
        f_n_sym = sympify(f_n)
        f_sym = sympify(f)
        
        # 1. Try symbolic limit of exact integral without Abs (works for positive integrands)
        try:
            integrand = (f_n_sym - f_sym)**p_sym
            integral_expr = integrate(integrand, (x, a_sym, b_sym))
            if not integral_expr.has(Integral):
                L = limit(integral_expr, n, oo)
                if L.is_number and Abs(L) > 0:
                    neg_q = True
                elif hasattr(L, 'min') and hasattr(L, 'max'):
                    if L.min != 0 or L.max != 0:
                        neg_q = True
        except Exception:
            pass

        # 2. Try symbolic limit of exact integral with Abs
        if not neg_q:
            try:
                integrand = Abs(f_n_sym - f_sym)**p_sym
                integral_expr = integrate(integrand, (x, a_sym, b_sym))
                if not integral_expr.has(Integral):
                    L = limit(integral_expr, n, oo)
                    if L.is_number and L > 0:
                        neg_q = True
                    elif hasattr(L, 'min') and hasattr(L, 'max'):
                        if L.min != 0 or L.max != 0:
                            neg_q = True
            except Exception:
                pass

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]