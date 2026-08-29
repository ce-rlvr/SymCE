import sympy
from sympy import Symbol, integrate, diff, solve, sympify, im, re
import math

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a dictionary or a tuple/list containing:
    (f, a, b, m, M)
    where f is a sympy expression in terms of x, and a, b, m, M are real numbers.
    """
    try:
        if isinstance(witness, dict):
            f = sympify(witness.get('f', 0))
            a = float(sympify(witness.get('a', 0)).evalf())
            b = float(sympify(witness.get('b', 0)).evalf())
            m = float(sympify(witness.get('m', 0)).evalf())
            M = float(sympify(witness.get('M', 0)).evalf())
        else:
            f = sympify(witness[0])
            a = float(sympify(witness[1]).evalf())
            b = float(sympify(witness[2]).evalf())
            m = float(sympify(witness[3]).evalf())
            M = float(sympify(witness[4]).evalf())
    except Exception:
        return [False, False, False]

    # H_1: f is a Riemann integrable real-valued function on the interval a to b
    try:
        h1 = False
        if a < b:
            integral_val = integrate(f, (x, a, b)).evalf()
            if integral_val.is_finite:
                im_part = float(im(integral_val).evalf())
                if abs(im_part) < 1e-9:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: m < 0 < M and m <= f(x) <= M for all x in the interval a to b
    try:
        h2 = False
        if m < 0 and M > 0:
            grid_points = [a + (b - a) * i / 100.0 for i in range(101)]
            all_vals = []
            for pt in grid_points:
                val = f.subs(x, pt).evalf()
                if abs(float(im(val).evalf())) < 1e-9:
                    all_vals.append(float(re(val).evalf()))
            
            try:
                df = diff(f, x)
                roots = solve(df, x)
                for r in roots:
                    try:
                        r_val = r.evalf()
                        if abs(float(im(r_val))) < 1e-9:
                            rf = float(re(r_val))
                            if a <= rf <= b:
                                val = f.subs(x, rf).evalf()
                                if abs(float(im(val).evalf())) < 1e-9:
                                    all_vals.append(float(re(val).evalf()))
                    except Exception:
                        continue
            except Exception:
                pass
            
            if all_vals and min(all_vals) >= m - 1e-7 and max(all_vals) <= M + 1e-7:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: integral of f(x)^2 dx > -mM(b-a)
    try:
        neg_q = False
        lhs_val = integrate(f**2, (x, a, b)).evalf()
        im_part = float(im(lhs_val).evalf())
        if abs(im_part) < 1e-9:
            lhs = float(re(lhs_val).evalf())
            rhs = -m * M * (b - a)
            if lhs > rhs + 1e-7:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a Riemann integrable real-valued function on the interval a to b",
    "H_2: There exist real numbers m and M with m < 0 < M such that m <= f(x) <= M for all x in the interval a to b",
    "¬Q: integral of f(x)^2 dx > -mM(b-a)"
]

N_HYP = 2
NEG_Q_INDEX = 2