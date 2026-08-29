import sympy
import math

# Top-level setup
# (No specific named objects are required for this real analysis theorem)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false Chebyshev's Inequality conjecture.
    The witness should be a dictionary or tuple providing:
      - f: list of function values (floats)
      - mu: list of measure values for each point (non-negative floats)
      - p: the exponent (float >= 1)
      - t: the threshold (float)
    """
    try:
        if isinstance(witness, dict):
            f = list(witness['f'])
            mu = list(witness['mu'])
            p = witness['p']
            t = witness['t']
        else:
            f = list(witness[0])
            mu = list(witness[1])
            p = witness[2]
            t = witness[3]
    except Exception:
        return [False, False, False]

    # H_1: (X, \Sigma, \mu) is a measure space
    try:
        h1 = False
        if len(f) == len(mu):
            h1 = all(float(m) >= 0 for m in mu)
    except Exception:
        h1 = False

    # H_2: f \in L^p(X, \mu) for some 1 \le p < \infty
    try:
        h2 = False
        p_float = float(p)
        if p_float >= 1 and p_float < float('inf'):
            integral = sum((abs(float(x))**p_float) * float(m) for x, m in zip(f, mu))
            if integral < float('inf'):
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: \mu(\{x \in X : |f(x)| \ge t\}) > \frac{1}{t^p} \int_X |f|^p \, d\mu  (or undefined)
    try:
        t_float = float(t)
        p_float = float(p)
        lhs = sum(float(m) for x, m in zip(f, mu) if abs(float(x)) >= t_float)
        
        if t_float == 0:
            neg_q = True
        else:
            t_pow = t_float ** p_float
            if isinstance(t_pow, complex):
                neg_q = True
            else:
                integral = sum((abs(float(x))**p_float) * float(m) for x, m in zip(f, mu))
                rhs = (1.0 / t_pow) * integral
                neg_q = not (lhs <= rhs)
    except Exception:
        # Any evaluation error (e.g., ZeroDivisionError) means the conclusion is undefined, thus fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a measure space",
    "H_2: f in L^p(X, mu) for some 1 <= p < infinity",
    "¬Q: mu({x in X : |f(x)| >= t}) > (1/t^p) integral |f|^p dmu or undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2