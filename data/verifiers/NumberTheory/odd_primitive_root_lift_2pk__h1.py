import math
import sympy
from sympy.ntheory import is_primitive_root, totient, n_order

def is_int(x):
    try:
        return int(x) == x and not isinstance(x, (float, bool))
    except Exception:
        return False

def check_prim_root(a, n):
    try:
        if n <= 1:
            return False
        res = is_primitive_root(a, n)
        if res is not None:
            return bool(res)
    except Exception:
        pass
    
    try:
        if math.gcd(int(a), int(n)) != 1:
            return False
        return n_order(a, n) == totient(n)
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (p, k, a) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
            a = witness.get('a')
        else:
            p, k, a = witness
    except Exception:
        return [False, False, False, False]

    # H_1: k is a positive integer
    try:
        h1_ok = is_int(k) and int(k) > 0
    except Exception:
        h1_ok = False

    # H_2: a is an odd integer
    try:
        h2_ok = is_int(a) and int(a) % 2 == 1
    except Exception:
        h2_ok = False

    # H_3: a is a primitive root modulo p^k
    try:
        if is_int(p) and is_int(k) and int(k) > 0 and is_int(a):
            modulus = int(p) ** int(k)
            h3_ok = check_prim_root(int(a), modulus)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: a is NOT a primitive root modulo 2p^k
    try:
        if is_int(p) and is_int(k) and int(k) > 0 and is_int(a):
            modulus2 = 2 * (int(p) ** int(k))
            neg_q_ok = not check_prim_root(int(a), modulus2)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: a is an odd integer",
    "H_3: a is a primitive root modulo p^k",
    "¬Q: a is not a primitive root modulo 2p^k"
]

N_HYP = 3
NEG_Q_INDEX = 3