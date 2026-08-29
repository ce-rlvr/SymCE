import math

# Top-level setup
# No named bindings needed for this number theory conjecture.

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of four integers: (a, b, x, y).
    """
    try:
        a, b, x, y = witness
    except Exception:
        return [False] * 5

    # H_1: b is a strictly positive integer
    try:
        h1 = (int(b) == b) and b > 0
    except Exception:
        h1 = False

    # H_2: \gcd(a, b) = 1
    try:
        h2 = (int(a) == a) and (int(b) == b) and math.gcd(int(a), int(b)) == 1
    except Exception:
        h2 = False

    # H_3: x is an integer such that ax \equiv 1 \pmod b
    try:
        h3 = (int(x) == x) and (int(a) * int(x)) % int(b) == 1 % int(b)
    except Exception:
        h3 = False

    # H_4: y is an integer such that by \equiv 1 \pmod a
    try:
        if int(y) != y:
            h4 = False
        else:
            a_int = int(a)
            b_int = int(b)
            y_int = int(y)
            if a_int == 0:
                h4 = (b_int * y_int == 1)
            else:
                h4 = ((b_int * y_int) % abs(a_int) == 1 % abs(a_int))
    except Exception:
        h4 = False

    # ¬Q: ax + by \equiv 1 \pmod{ab} must FAIL
    try:
        a_int = int(a)
        b_int = int(b)
        x_int = int(x)
        y_int = int(y)
        
        if a_int * b_int == 0:
            # Modulo 0 is undefined in standard programming, causing the conclusion to fail.
            q_ok = False
        else:
            ab = abs(a_int * b_int)
            q_ok = ((a_int * x_int + b_int * y_int) % ab == 1 % ab)
            
        neg_q = not q_ok
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: b is a strictly positive integer",
    "H_2: gcd(a, b) = 1",
    "H_3: x is an integer such that ax = 1 mod b",
    "H_4: y is an integer such that by = 1 mod a",
    "¬Q: ax + by is not 1 mod ab"
]

N_HYP = 4
NEG_Q_INDEX = 4