import math
from sympy.ntheory import mobius

def conditions(witness):
    """
    Given a witness (m, n, q), checks the hypotheses and the negated conclusion.
    """
    try:
        m, n, q = witness
        # Convert integer-like types to int for exact arithmetic
        if hasattr(m, 'is_integer') and m.is_integer:
            m = int(m)
        if hasattr(n, 'is_integer') and n.is_integer:
            n = int(n)
        if hasattr(q, 'is_integer') and q.is_integer:
            q = int(q)
    except Exception:
        return [False, False, False, False]

    # H_1: q is an integer
    try:
        h1 = isinstance(q, int)
    except Exception:
        h1 = False

    # H_2: c_n(q) is the Ramanujan sum modulo n
    # We interpret this as m and n being valid integers so the sum is well-defined.
    try:
        h2 = isinstance(m, int) and isinstance(n, int)
    except Exception:
        h2 = False

    # H_3: \gcd(m, n) = 1
    try:
        h3 = math.gcd(m, n) == 1
    except Exception:
        h3 = False

    # ¬Q: c_{mn}(q) != c_m(q) c_n(q)
    try:
        def ramanujan_sum(k, q_val):
            # The standard Ramanujan sum is defined for positive integers k.
            # For k <= 0, the sum over 1 <= a <= k is empty, yielding 0.
            if k <= 0:
                return 0
            ans = 0
            g = math.gcd(k, q_val)
            for d in range(1, g + 1):
                if g % d == 0:
                    ans += d * mobius(k // d)
            return ans

        c_mn = ramanujan_sum(m * n, q)
        c_m = ramanujan_sum(m, q)
        c_n = ramanujan_sum(n, q)
        
        neg_q = c_mn != c_m * c_n
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: q is an integer",
    "H_2: c_n(q) is the Ramanujan sum modulo n",
    "H_3: gcd(m, n) = 1",
    "¬Q: c_{mn}(q) != c_m(q) c_n(q)"
]

N_HYP = 3
NEG_Q_INDEX = 3