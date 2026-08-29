import sympy
from sympy import oo

n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    # H1: (x_n) is a sequence of real numbers
    h1_ok = False
    try:
        h1_ok = True
        for i in range(100, 105):
            val = witness.subs(n, i).evalf()
            if not val.is_real:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H2: lim_{n \to \infty} (x_{n+1} - x_n) = 0
    h2_ok = False
    try:
        diff = (witness.subs(n, n+1) - witness).doit().simplify()
        lim = sympy.limit(diff, n, oo)
        if lim == 0:
            h2_ok = True
        else:
            v = abs(complex(diff.subs(n, 10**5).evalf()))
            if v < 1e-4:
                h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The set of subsequential limits is NOT a closed interval
    # By the true theorem, if the sequence is bounded and H2 holds, it IS a closed interval.
    # Thus, the conclusion fails (neg_Q is True) if and only if the sequence is unbounded.
    neg_q_ok = False
    try:
        w_doit = witness.doit()
        lim_inf = sympy.limit(w_doit, n, oo)
        if lim_inf in [oo, -oo]:
            neg_q_ok = True
        elif hasattr(lim_inf, 'min') and hasattr(lim_inf, 'max'):
            if lim_inf.min == -oo or lim_inf.max == oo:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: (x_n) is a sequence of real numbers", "H_2: lim_{n -> oo} (x_{n+1} - x_n) = 0", "¬Q: The set of subsequential limits of (x_n) does not form a closed interval"]

N_HYP = 2
NEG_Q_INDEX = 2