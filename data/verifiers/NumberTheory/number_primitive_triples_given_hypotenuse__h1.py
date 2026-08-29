import math
from sympy.ntheory import factorint

# Top-level setup
# No named bindings needed for Number Theory; use integers directly.

def get_k(c):
    try:
        c = int(c)
    except Exception:
        return 0
    if c == 0:
        return 0
    c = abs(c)
    if c == 1:
        return 0
    return len(factorint(c))

def count_primitive_triples(c):
    try:
        c = int(c)
    except Exception:
        return 0
    if c == 0:
        return 0
    c = abs(c)
    
    # For reasonably small c, we can just count the solutions directly.
    # This also correctly handles edge cases like c=1 where a=0 is allowed.
    if c <= 100000:
        count = 0
        limit = int(c / math.sqrt(2))
        for a in range(0, limit + 1):
            b_sq = c*c - a*a
            if b_sq < 0:
                continue
            b = math.isqrt(b_sq)
            if b*b == b_sq:
                if math.gcd(a, b) == 1:
                    count += 1
        return count
    else:
        # For large c, we use the known number theory formula.
        # A primitive triple exists iff all prime factors are 1 mod 4.
        factors = factorint(c)
        if 2 in factors:
            return 0
        for p in factors:
            if p % 4 == 3:
                return 0
        return 2 ** (len(factors) - 1)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness can be a tuple (c, k), a dict, or just the integer c.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            c, k = witness
        elif isinstance(witness, dict):
            c = witness['c']
            k = witness['k']
        else:
            c = int(witness)
            k = get_k(c)
    except Exception:
        return [False, False, False]

    # H_1: c is the hypotenuse of at least one primitive Pythagorean triple
    try:
        count = count_primitive_triples(c)
        h1_ok = bool(count >= 1)
    except Exception:
        h1_ok = False

    # H_2: k is the number of distinct prime factors of c
    try:
        actual_k = get_k(c)
        h2_ok = bool(k == actual_k)
    except Exception:
        h2_ok = False

    # ¬Q: The number of distinct primitive Pythagorean triples (up to the order of legs) 
    # having hypotenuse c is NOT exactly 2^{k-1}
    try:
        expected = 2 ** (k - 1)
        neg_q_ok = bool(count != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: c is the hypotenuse of at least one primitive Pythagorean triple",
    "H_2: k is the number of distinct prime factors of c",
    "¬Q: The number of distinct primitive Pythagorean triples (up to the order of legs) having hypotenuse c is not exactly 2^{k-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2