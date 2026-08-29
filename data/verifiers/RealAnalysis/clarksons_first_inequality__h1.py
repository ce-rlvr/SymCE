import sympy as sp

# Top-level setup
# We define standard objects that might be used in the witness.
# For this real analysis conjecture, the witness will likely be a tuple (p, f, g)
# where f and g are represented as lists or tuples of values (e.g., for a discrete measure space).
# No special group or ring bindings are needed, but we provide standard ones just in case.
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (p, f, g), checks the remaining hypotheses and the negated conclusion.
    We assume f and g are iterables of numbers representing functions on a discrete space with counting measure.
    """
    try:
        # Unpack witness
        if len(witness) != 3:
            return [False, False, False]
        p, f, g = witness
    except Exception:
        return [False, False, False]

    # H1: Let p be a real number such that 2 <= p < \infty
    try:
        p_val = float(p)
        h1_ok = (2.0 <= p_val < float('inf'))
    except Exception:
        h1_ok = False

    # H2: Let f and g be functions in L^p(\Omega, \mu)
    try:
        # Check if f and g are iterables of numbers
        f_vals = [complex(x) for x in f]
        g_vals = [complex(x) for x in g]
        if len(f_vals) != len(g_vals) or len(f_vals) == 0:
            h2_ok = False
        else:
            # In a finite discrete space, any finite-valued function is in L^p
            h2_ok = all(abs(x) < float('inf') for x in f_vals) and all(abs(x) < float('inf') for x in g_vals)
    except Exception:
        h2_ok = False

    # Negated Conclusion:
    # ||(f+g)/2||_p^p + ||(f-g)/2||_p^p > 1/2 (||f||_p^p + ||g||_p^p)
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            p_val = float(p)
            
            def norm_p_p(vec):
                return sum(abs(x)**p_val for x in vec)
            
            f_plus_g_over_2 = [(x + y) / 2.0 for x, y in zip(f_vals, g_vals)]
            f_minus_g_over_2 = [(x - y) / 2.0 for x, y in zip(f_vals, g_vals)]
            
            lhs = norm_p_p(f_plus_g_over_2) + norm_p_p(f_minus_g_over_2)
            rhs = 0.5 * (norm_p_p(f_vals) + norm_p_p(g_vals))
            
            # We use a small tolerance to avoid floating point inaccuracies,
            # but since we want the conclusion to strictly FAIL, we check LHS > RHS + tol
            neg_q_ok = bool(lhs > rhs + 1e-9)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a real number such that 2 <= p < \\infty",
    "H_2: f and g are functions in L^p(\\Omega, \\mu)",
    "¬Q: ||(f+g)/2||_p^p + ||(f-g)/2||_p^p > 1/2 (||f||_p^p + ||g||_p^p)"
]

N_HYP = 2
NEG_Q_INDEX = 2