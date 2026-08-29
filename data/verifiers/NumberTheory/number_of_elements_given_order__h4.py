import sympy
import sympy.ntheory
import math

# Top-level setup (no named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        n, d = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n > 1 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # H_2: There exists at least one primitive root modulo n
    try:
        if h1:
            try:
                sympy.ntheory.primitive_root(int(n))
                h2 = True
            except ValueError:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: d is a positive integer
    try:
        h3 = isinstance(d, (int, sympy.Integer)) and d > 0
    except Exception:
        h3 = False

    # neg_Q: The number of incongruent integers modulo n that have multiplicative order d modulo n is NOT equal to \phi(d)
    try:
        if h1 and h3:
            count = 0
            n_int = int(n)
            d_int = int(d)
            for a in range(1, n_int):
                if math.gcd(a, n_int) == 1:
                    if sympy.ntheory.n_order(a, n_int) == d_int:
                        count += 1
            neg_q = bool(count != sympy.totient(d_int))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "H_2: There exists at least one primitive root modulo n",
    "H_3: d is a positive integer",
    "¬Q: The number of incongruent integers modulo n that have multiplicative order d modulo n is not exactly phi(d)"
]

N_HYP = 3
NEG_Q_INDEX = 3