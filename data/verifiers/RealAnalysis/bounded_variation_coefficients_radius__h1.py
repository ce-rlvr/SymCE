import sympy

# Top-level setup
n = sympy.Symbol('n', integer=True, nonnegative=True)

CONDITION_LABELS = [
    "H_1: sum_{n=0}^infty |a_{n+1} - a_n| < infty",
    "¬Q: The radius of convergence is < 1 OR the series diverges at x = -1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H1: sum |a_{n+1} - a_n| < oo
    h1_ok = False
    try:
        diff = sympy.simplify(witness.subs(n, n+1) - witness)
        if diff == 0:
            h1_ok = True
        else:
            abs_diff = sympy.Abs(diff)
            sum_abs = sympy.Sum(abs_diff, (n, 0, sympy.oo))
            conv = sum_abs.is_convergent()
            if conv is True:
                h1_ok = True
            elif conv is False:
                h1_ok = False
            else:
                # Fallback if is_convergent() cannot decide
                val = sum_abs.doit()
                if val.is_finite:
                    h1_ok = True
    except Exception:
        pass

    # neg_Q: R < 1 OR diverges at x = -1
    neg_q_ok = False
    try:
        term_limit = sympy.limit(witness, n, sympy.oo)
        # If the limit is not zero, the terms of sum a_n (-1)^n do not go to zero,
        # so the series diverges at x = -1.
        if term_limit != 0:
            neg_q_ok = True
        else:
            # Check if radius of convergence R < 1
            try:
                ratio = sympy.Abs(witness / witness.subs(n, n+1))
                R = sympy.limit(ratio, n, sympy.oo)
                if R < 1:
                    neg_q_ok = True
            except Exception:
                pass
            
            # If not already True, check convergence of sum a_n (-1)^n directly
            if not neg_q_ok:
                series_sum = sympy.Sum(witness * (-1)**n, (n, 0, sympy.oo))
                if series_sum.is_convergent() is False:
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]