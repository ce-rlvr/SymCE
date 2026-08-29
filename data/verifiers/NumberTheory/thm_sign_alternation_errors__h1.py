import sympy
from sympy.ntheory import continued_fraction_iterator, continued_fraction_convergents
import itertools

# Top-level setup
# (No specific named objects needed for this Number Theory problem)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (alpha, n, p_n, q_n), a tuple (alpha, n), or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness['alpha']
            n = witness['n']
            if 'p_n' in witness and 'q_n' in witness:
                p_n = witness['p_n']
                q_n = witness['q_n']
            else:
                n_int = int(n)
                cf_iter = continued_fraction_iterator(alpha)
                cf_n = list(itertools.islice(cf_iter, n_int + 1))
                if len(cf_n) < n_int + 1:
                    p_n, q_n = None, None
                else:
                    convergents = list(continued_fraction_convergents(cf_n))
                    c = convergents[-1]
                    p_n, q_n = c.p, c.q
        else:
            if len(witness) == 4:
                alpha, n, p_n, q_n = witness
            elif len(witness) == 2:
                alpha, n = witness
                n_int = int(n)
                cf_iter = continued_fraction_iterator(alpha)
                cf_n = list(itertools.islice(cf_iter, n_int + 1))
                if len(cf_n) < n_int + 1:
                    p_n, q_n = None, None
                else:
                    convergents = list(continued_fraction_convergents(cf_n))
                    c = convergents[-1]
                    p_n, q_n = c.p, c.q
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: p_n/q_n is the n-th convergent of the simple continued fraction expansion of alpha
    try:
        if p_n is None or q_n is None:
            h1 = False
        else:
            n_int = int(n)
            cf_iter = continued_fraction_iterator(alpha)
            cf_n = list(itertools.islice(cf_iter, n_int + 1))
            if len(cf_n) < n_int + 1:
                h1 = False
            else:
                convergents = list(continued_fraction_convergents(cf_n))
                c = convergents[-1]
                h1 = (c.p == p_n) and (c.q == q_n)
    except Exception:
        h1 = False

    # H2: n is a non-negative integer
    try:
        h2 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and int(n) >= 0
    except Exception:
        h2 = False

    # neg_Q: The quantity q_n * alpha - p_n is NOT strictly positive if n is even, and strictly negative if n is odd
    try:
        if p_n is None or q_n is None:
            neg_q = False
        else:
            val = q_n * alpha - p_n
            n_int = int(n)
            if n_int % 2 == 0:
                try:
                    q_holds = bool(val > 0)
                except TypeError:
                    q_holds = bool(val.evalf() > 0)
            else:
                try:
                    q_holds = bool(val < 0)
                except TypeError:
                    q_holds = bool(val.evalf() < 0)
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p_n/q_n is the n-th convergent of the simple continued fraction expansion of alpha",
    "H_2: n is a non-negative integer",
    "¬Q: The quantity q_n * alpha - p_n is NOT strictly positive if n is even, and strictly negative if n is odd"
]

N_HYP = 2
NEG_Q_INDEX = 2