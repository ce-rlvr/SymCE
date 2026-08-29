import sympy as sp

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on [1, oo)",
    "H_2: f is monotonically decreasing on [1, oo)",
    "H_3: n is a positive integer",
    "¬Q: The integral test bounds fail"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (f, n) where f is a sympy expression in terms of x,
    and n is an integer, checks if it is a counterexample to the false conjecture.
    """
    try:
        f_expr, n_val = witness
    except Exception:
        return [False, False, False, False]

    x = sp.Symbol('x', real=True)

    # H_1: f is a real-valued function defined on [1, oo)
    # We check if f can be evaluated at a few points in [1, oo) and yields real numbers.
    try:
        h1_ok = True
        for test_pt in [1, 2, 3.5, 10, 100]:
            val = f_expr.subs(x, test_pt)
            if not val.is_real or val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: f is monotonically decreasing on [1, oo)
    # We check if the derivative is <= 0 on [1, oo).
    try:
        f_prime = sp.diff(f_expr, x)
        # A simple heuristic check for monotonicity:
        h2_ok = True
        for test_pt in [1, 1.5, 2, 3.14, 10, 50]:
            deriv_val = f_prime.subs(x, test_pt)
            if deriv_val > 0:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # H_3: n is a positive integer
    try:
        h3_ok = isinstance(n_val, int) and n_val > 0
    except Exception:
        h3_ok = False

    # ¬Q: The conclusion fails
    # Conclusion: Integral(f, (x, 1, n+1)) <= Sum(f(k), (k, 1, n)) <= f(1) + Integral(f, (x, 1, n))
    try:
        if not h3_ok:
            neg_q = False
        else:
            integral_1_to_n_plus_1 = sp.integrate(f_expr, (x, 1, n_val + 1))
            integral_1_to_n = sp.integrate(f_expr, (x, 1, n_val))
            
            sum_f = sum(f_expr.subs(x, k) for k in range(1, n_val + 1))
            f_1 = f_expr.subs(x, 1)
            
            left_bound_ok = bool(integral_1_to_n_plus_1 <= sum_f)
            right_bound_ok = bool(sum_f <= f_1 + integral_1_to_n)
            
            # The conclusion holds if BOTH bounds are satisfied.
            # The negation is True if AT LEAST ONE bound fails.
            neg_q = not (left_bound_ok and right_bound_ok)
    except Exception:
        # If integration or comparison fails, we cannot conclusively say the bounds hold,
        # but for a verifier we return False on exception.
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]