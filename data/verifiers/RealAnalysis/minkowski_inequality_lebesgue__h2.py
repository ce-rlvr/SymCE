import sympy
import math

def lp_norm(vec, p):
    p_val = float(p)
    if p_val <= 0:
        raise ValueError("p must be > 0")
    if p_val == float('inf'):
        return max((abs(float(x)) for x in vec), default=0.0)
    return sum(abs(float(x))**p_val for x in vec)**(1.0/p_val)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Minkowski's Inequality
    (where the hypothesis p >= 1 was dropped).
    
    The witness is expected to be a tuple (p, f, g) or a dictionary with keys 'p', 'f', 'g',
    where p is a real number > 0, and f and g are iterables of numbers of the same length
    representing functions on a discrete measure space.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            f = witness['f']
            g = witness['g']
        else:
            if len(witness) == 3:
                p, f, g = witness
            elif len(witness) == 6:
                _, _, _, p, f, g = witness
            else:
                p, f, g = witness[-3:]
    except Exception:
        return [False, False, False, False]

    # H1: (X, Sigma, mu) is a measure space
    # We implicitly use a finite discrete space with counting measure.
    try:
        f_list = list(f)
        g_list = list(g)
        h1 = len(f_list) == len(g_list) and len(f_list) > 0
    except Exception:
        h1 = False
        f_list = []
        g_list = []

    # H2: f in L^p(X, mu)
    try:
        norm_f = lp_norm(f_list, p)
        h2 = math.isfinite(norm_f)
    except Exception:
        h2 = False

    # H3: g in L^p(X, mu)
    try:
        norm_g = lp_norm(g_list, p)
        h3 = math.isfinite(norm_g)
    except Exception:
        h3 = False

    # ¬Q: The sum f + g is NOT in L^p(X, mu) OR ||f + g||_p > ||f||_p + ||g||_p
    try:
        fg_list = [float(x) + float(y) for x, y in zip(f_list, g_list)]
        norm_fg = lp_norm(fg_list, p)
        
        if not math.isfinite(norm_fg):
            neg_q = True
        else:
            # We use a small epsilon to avoid false positives due to floating-point inaccuracies.
            # A true counterexample (e.g., p=0.5) will violate the inequality by a large margin.
            neg_q = norm_fg > norm_f + norm_g + 1e-7
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a measure space",
    "H_2: f in L^p(X, mu)",
    "H_3: g in L^p(X, mu)",
    "¬Q: f + g not in L^p(X, mu) or ||f + g||_p > ||f||_p + ||g||_p"
]

N_HYP = 3
NEG_Q_INDEX = 3