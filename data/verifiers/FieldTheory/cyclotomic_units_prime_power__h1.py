import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'Cyclotomic Units of Prime Power Index' (with 'p is a prime' dropped).
    
    Witness is expected to be a tuple or dict providing (p, k, a).
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
            a = witness.get('a')
        else:
            if len(witness) < 3:
                return [False, False, False, False]
            p, k, a = witness[:3]
    except Exception:
        return [False, False, False, False]

    # H_1: k >= 1 is an integer
    try:
        h1 = (int(k) == k) and (k >= 1)
    except Exception:
        h1 = False

    # H_2: \zeta_{p^k} is a primitive p^k-th root of unity
    # A primitive n-th root of unity exists in C if and only if n >= 1.
    try:
        h2 = (int(p) == p) and (p**k >= 1)
    except Exception:
        h2 = False

    # H_3: a is an integer such that \gcd(a, p) = 1
    try:
        h3 = (int(a) == a) and (math.gcd(int(a), int(p)) == 1)
    except Exception:
        h3 = False

    # ¬Q: The element (\zeta_{p^k}^a - 1) / (\zeta_{p^k} - 1) is NOT a unit in \mathbb{Z}[\zeta_{p^k}]
    # For any n >= 2, if \gcd(a, n) = 1, the element is always a unit (cyclotomic unit).
    # The conclusion only fails when n = p^k = 1, where \zeta_1 = 1, making the element 0/0 (undefined, hence not a unit).
    try:
        n = p**k
        if n == 1:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k >= 1 is an integer",
    "H_2: \\zeta_{p^k} is a primitive p^k-th root of unity",
    "H_3: a is an integer such that \\gcd(a, p) = 1",
    "¬Q: The element is not a unit in the ring of integers"
]

N_HYP = 3
NEG_Q_INDEX = 3