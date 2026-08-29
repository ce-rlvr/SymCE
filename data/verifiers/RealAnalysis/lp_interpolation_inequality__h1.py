import math
import sympy as sp

oo = sp.oo

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should provide p, q, r, theta, f, and optionally mu.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
            r = witness['r']
            theta = witness['theta']
            f = witness['f']
            if not hasattr(f, '__iter__') or isinstance(f, str):
                f = [f]
            mu = witness.get('mu', [1] * len(f))
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                p, q, r, theta, f = witness
                if not hasattr(f, '__iter__') or isinstance(f, str):
                    f = [f]
                mu = [1] * len(f)
            elif len(witness) == 6:
                p, q, r, theta, f, mu = witness
                if not hasattr(f, '__iter__') or isinstance(f, str):
                    f = [f]
                if not hasattr(mu, '__iter__') or isinstance(mu, str):
                    mu = [mu]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def get_norm(f, mu, p):
        if not f:
            return 0.0
        if p == float('inf') or str(p) == 'oo':
            valid_x = [abs(float(x)) for x, m in zip(f, mu) if float(m) != 0]
            return float(max(valid_x)) if valid_x else 0.0
        else:
            # For signed measures (which is the dropped hypothesis allowing the counterexample),
            # we compute the absolute value of the integral before taking the 1/p power.
            s = sum(float(m) * (abs(float(x))**float(p)) for x, m in zip(f, mu))
            return abs(s)**(1/float(p))

    # H_1: 1 <= p < q < r <= infinity
    try:
        p_val = float(p)
        q_val = float(q)
        r_val = float('inf') if str(r) == 'oo' else float(r)
        h1 = bool(1 <= p_val < q_val < r_val <= float('inf'))
    except Exception:
        h1 = False

    # H_2: f in L^p(X, mu) \cap L^r(X, mu)
    try:
        norm_p = get_norm(f, mu, p)
        norm_r = get_norm(f, mu, r)
        h2 = bool(norm_p < float('inf') and norm_r < float('inf'))
    except Exception:
        h2 = False

    # H_3: theta in (0, 1) satisfies 1/q = theta/p + (1-theta)/r
    try:
        t = float(theta)
        p_val = float(p)
        q_val = float(q)
        r_val = float('inf') if str(r) == 'oo' else float(r)
        if 0 < t < 1:
            left = 1 / q_val
            right = t / p_val + (1 - t) / r_val if r_val != float('inf') else t / p_val
            h3 = bool(math.isclose(left, right, rel_tol=1e-5, abs_tol=1e-5))
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: f not in L^q(X, mu) OR ||f||_q > ||f||_p^theta * ||f||_r^{1-theta}
    try:
        norm_q = get_norm(f, mu, q)
        if norm_q == float('inf'):
            neg_q = True
        else:
            norm_p = get_norm(f, mu, p)
            norm_r = get_norm(f, mu, r)
            t = float(theta)
            rhs = (norm_p ** t) * (norm_r ** (1 - t))
            neg_q = bool(norm_q > rhs + 1e-7)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: 1 <= p < q < r <= infinity",
    "H_2: f in L^p(X, mu) and L^r(X, mu)",
    "H_3: theta in (0, 1) satisfies 1/q = theta/p + (1-theta)/r",
    "¬Q: f not in L^q(X, mu) or ||f||_q > ||f||_p^theta ||f||_r^{1-theta}"
]

N_HYP = 3
NEG_Q_INDEX = 3