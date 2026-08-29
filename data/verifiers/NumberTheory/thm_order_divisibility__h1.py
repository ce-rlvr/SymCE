import math
import sympy

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

def is_int(x):
    if isinstance(x, bool):
        return False
    try:
        return int(x) == x
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 4 + [False]
        a, n, k = witness
    except Exception:
        return [False] * 4 + [False]

    # H1: a is an integer
    try:
        h1 = is_int(a)
    except Exception:
        h1 = False

    # H2: gcd(a, n) = 1
    try:
        h2 = is_int(n) and math.gcd(int(a), int(n)) == 1
    except Exception:
        h2 = False

    # H3: k is a positive integer
    try:
        h3 = is_int(k) and int(k) > 0
    except Exception:
        h3 = False

    # H4: a^k \equiv 1 \pmod n
    try:
        a_int = int(a)
        n_int = int(n)
        k_int = int(k)
        if n_int == 0:
            h4 = (abs(a_int) == 1 and a_int**k_int == 1)
        else:
            h4 = (pow(a_int, k_int, n_int) == 1 % n_int)
    except Exception:
        h4 = False

    # neg_Q: The multiplicative order of a modulo n does NOT divide k
    try:
        a_int = int(a)
        n_int = int(n)
        k_int = int(k)
        from sympy.ntheory import n_order
        try:
            order = n_order(a_int, n_int)
            neg_q = (k_int % order != 0)
        except ValueError:
            # n_order raises ValueError if n <= 1 or gcd(a, n) != 1.
            # If the order is undefined (e.g., for n = 1), the statement 
            # "the order divides k" is false, making its negation true.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: gcd(a, n) = 1",
    "H_3: k is a positive integer",
    "H_4: a^k = 1 (mod n)",
    "¬Q: The multiplicative order of a modulo n does not divide k (or is undefined)"
]

N_HYP = 4
NEG_Q_INDEX = 4