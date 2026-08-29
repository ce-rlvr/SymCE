import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g, p) where f and g are lists of numbers
    representing functions on a discrete measure space, and p is a real number.
    """
    try:
        f, g, p = witness
    except Exception:
        return [False, False, False]

    # H_1: (X, Sigma, mu) is a measure space
    # We verify this by checking that f and g are valid vectors of the same length
    try:
        if len(f) != len(g) or len(f) == 0:
            h1 = False
        else:
            # Ensure all elements are numeric
            f_val = [float(x) for x in f]
            g_val = [float(x) for x in g]
            h1 = True
    except Exception:
        h1 = False

    # H_2: p is a real number such that 1 <= p <= 2
    try:
        p_val = float(p)
        h2 = (1.0 <= p_val <= 2.0)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails at the witness
    # Conclusion: ||f+g||_p^p + ||f-g||_p^p >= (||f||_p + ||g||_p)^p + | ||f||_p - ||g||_p |^p
    # Negation: ||f+g||_p^p + ||f-g||_p^p < (||f||_p + ||g||_p)^p + | ||f||_p - ||g||_p |^p
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            def lp_norm(vec, p):
                return sum(abs(x)**p for x in vec)**(1/p)

            norm_f = lp_norm(f_val, p_val)
            norm_g = lp_norm(g_val, p_val)
            
            f_plus_g = [x + y for x, y in zip(f_val, g_val)]
            f_minus_g = [x - y for x, y in zip(f_val, g_val)]
            
            lhs = sum(abs(x)**p_val for x in f_plus_g) + sum(abs(x)**p_val for x in f_minus_g)
            rhs = (norm_f + norm_g)**p_val + abs(norm_f - norm_g)**p_val
            
            # Check if LHS < RHS (with a small tolerance for floating point errors)
            neg_q = lhs < rhs - 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a measure space (f and g are valid vectors)",
    "H_2: p is a real number such that 1 <= p <= 2",
    "¬Q: ||f+g||_p^p + ||f-g||_p^p < (||f||_p + ||g||_p)^p + | ||f||_p - ||g||_p |^p"
]

N_HYP = 2
NEG_Q_INDEX = 2