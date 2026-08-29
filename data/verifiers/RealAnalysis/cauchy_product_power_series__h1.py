import sympy
from sympy.abc import n, x
import math
import cmath

def eval_seq(seq, i):
    if callable(seq):
        val = seq(i)
    elif isinstance(seq, (list, tuple)):
        val = seq[i] if i < len(seq) else 0
    elif hasattr(seq, 'subs'):
        val = seq.subs(n, i).evalf()
    else:
        val = seq
    return complex(val)

def eval_func(func, val):
    if callable(func):
        res = func(val)
    elif hasattr(func, 'subs'):
        res = func.subs(x, val).evalf()
    else:
        res = func
    return complex(res)

def conditions(witness):
    try:
        a = witness['a']
        b = witness['b']
        c = witness['c']
        R1 = float(witness['R1'])
        R2 = float(witness['R2'])
        f = witness['f']
        g = witness['g']
    except Exception:
        return [False, False]

    # H1: c_n = sum_{k=0}^n a_k b_{n-k}
    h1_ok = True
    try:
        for i in range(50):
            expected_c = sum(eval_seq(a, k) * eval_seq(b, i - k) for k in range(i + 1))
            actual_c = eval_seq(c, i)
            if abs(actual_c - expected_c) > 1e-7:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: conclusion fails
    # The conclusion is that the series converges absolutely for all |x| < min(R1, R2) and sums to f(x)g(x).
    # We check if there is an x with |x| < min(R1, R2) where it diverges or sums to a different value.
    neg_q = False
    try:
        R_min = min(R1, R2)
        if 'x' in witness:
            x_val = complex(witness['x'])
        else:
            if R_min > 0 and R_min != float('inf'):
                x_val = R_min / 2.0
            elif R_min == float('inf'):
                x_val = 1.0
            else:
                x_val = 0.0

        if abs(x_val) < R_min:
            try:
                N = 1000
                terms = [eval_seq(c, i) * (x_val ** i) for i in range(N)]
                abs_terms = [abs(t) for t in terms]
                
                # If the terms do not decay sufficiently, the series does not converge absolutely
                diverges = abs_terms[-1] > 1e-4
                if diverges:
                    neg_q = True
                else:
                    series_sum = sum(terms)
                    expected_sum = eval_func(f, x_val) * eval_func(g, x_val)
                    if abs(series_sum - expected_sum) > 1e-4:
                        neg_q = True
            except OverflowError:
                # Overflow during evaluation implies divergence
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: c_n = \\sum_{k=0}^{n} a_k b_{n-k} for all n \\geq 0",
    "¬Q: The series \\sum c_n x^n does not converge absolutely for some |x| < min(R1, R2) or its sum is not f(x)g(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1