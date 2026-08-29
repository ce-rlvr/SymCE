import sympy
from sympy import sqrt, Abs
from sympy.ntheory.continued_fraction import continued_fraction_iterator, continued_fraction_convergents

def conditions(witness):
    """
    Given a witness (x, n), checks the hypotheses and the negated conclusion.
    """
    try:
        x, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: x is an irrational number
    try:
        h1 = x.is_irrational
        if h1 is None:
            h1 = False
        else:
            h1 = bool(h1)
    except Exception:
        h1 = False
        
    # H_2: n >= 1 is an integer
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    # ¬Q: None of the convergents p_k/q_k for k in {n, n+1, n+2} satisfies |x - p_k/q_k| < 1 / (sqrt(5) q_k^2)
    try:
        cf = continued_fraction_iterator(x)
        convs = continued_fraction_convergents(cf)
        
        p_q_list = []
        for i, frac in enumerate(convs):
            if i >= n and i <= n + 2:
                p_q_list.append(frac)
            if i > n + 2:
                break
                
        if len(p_q_list) < 3:
            neg_q = False
        else:
            any_satisfies = False
            for frac in p_q_list:
                q = frac.q
                diff = Abs(x - frac).evalf(100)
                threshold = (1 / (sqrt(5) * q**2)).evalf(100)
                if diff < threshold:
                    any_satisfies = True
                    break
            neg_q = not any_satisfies
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "H_2: n >= 1 is an integer",
    "¬Q: None of the convergents p_k/q_k for k in {n, n+1, n+2} satisfies |x - p_k/q_k| < 1 / (sqrt(5) q_k^2)"
]

N_HYP = 2
NEG_Q_INDEX = 2