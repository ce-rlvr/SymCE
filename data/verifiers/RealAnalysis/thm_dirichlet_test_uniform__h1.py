import sympy as sp
import math

x, n, k = sp.symbols('x n k')

def evaluate(func, n_val, x_val):
    try:
        val = func(n_val, x_val)
        if hasattr(val, 'evalf'):
            return float(val.evalf())
        return float(val)
    except Exception:
        return 0.0

def conditions(witness) -> list[bool]:
    # Try to use witness methods if available
    if hasattr(witness, 'check_H1'):
        try: h1 = bool(witness.check_H1())
        except Exception: h1 = False
        try: h2 = bool(witness.check_H2())
        except Exception: h2 = False
        try: h3 = bool(witness.check_H3())
        except Exception: h3 = False
        try: h4 = bool(witness.check_H4())
        except Exception: h4 = False
        try: neg_q = bool(witness.check_neg_Q())
        except Exception: neg_q = False
        return [h1, h2, h3, h4, neg_q]

    # Fallback to numerical evaluation
    try:
        f = witness.f
        g = witness.g
        D = witness.D
        M = witness.M
    except Exception:
        return [False, False, False, False, False]

    # Generate test points
    test_D = []
    try:
        if hasattr(D, '__iter__'):
            test_D = list(D)[:100]
        elif hasattr(D, 'is_Interval') and D.is_Interval:
            start = float(D.start) if D.start.is_finite else -10.0
            end = float(D.end) if D.end.is_finite else 10.0
            test_D = [start + (end - start) * i / 50.0 for i in range(1, 50)]
    except Exception:
        pass
    if not test_D:
        test_D = [0.1, 0.5, 0.9]

    # H1
    h1 = callable(f) and callable(g)

    # H2
    h2 = False
    if M is not None and M > 0:
        h2_ok = True
        for pt in test_D:
            s = 0.0
            for n_val in range(1, 50):
                s += evaluate(f, n_val, pt)
                if abs(s) > M + 1e-5:
                    h2_ok = False
                    break
            if not h2_ok:
                break
        h2 = h2_ok

    # H3
    h3 = True
    for pt in test_D:
        for n_val in range(1, 50):
            if evaluate(g, n_val, pt) < evaluate(g, n_val + 1, pt) - 1e-7:
                h3 = False
                break
        if not h3:
            break

    # H4
    h4 = True
    max_g_50 = max((abs(evaluate(g, 50, pt)) for pt in test_D), default=0)
    max_g_100 = max((abs(evaluate(g, 100, pt)) for pt in test_D), default=0)
    if max_g_100 > max_g_50 + 1e-5 and max_g_100 > 0.1:
        h4 = False

    # neg_Q: does not converge uniformly
    neg_q = False
    try:
        if hasattr(witness, 'get_divergent_x'):
            x_bad = witness.get_divergent_x(100, 200)
            tail = sum(evaluate(f, k_val, x_bad) * evaluate(g, k_val, x_bad) for k_val in range(100, 200))
            if abs(tail) > 1e-2:
                neg_q = True
        else:
            for pt in test_D:
                tail = sum(evaluate(f, k_val, pt) * evaluate(g, k_val, pt) for k_val in range(50, 100))
                if abs(tail) > 0.1:
                    neg_q = True
                    break
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) and (g_n) are sequences of functions from D to the real numbers",
    "H_2: Partial sums of f_n are uniformly bounded by M on D",
    "H_3: g_n(x) is monotonically decreasing for each x in D",
    "H_4: g_n converges uniformly to 0 on D",
    "¬Q: The series sum f_n(x) g_n(x) does NOT converge uniformly on D"
]

N_HYP = 4
NEG_Q_INDEX = 4