import sympy
import math

def is_integer(val):
    if isinstance(val, (int, sympy.Integer)):
        return True
    if hasattr(val, 'is_integer') and val.is_integer:
        return True
    return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    "If x, y are coprime integers and p divides x^2 + y^2, then the prime p is congruent to 1 mod 4."
    """
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            p = witness['p']
        elif hasattr(witness, 'x') and hasattr(witness, 'y') and hasattr(witness, 'p'):
            x = witness.x
            y = witness.y
            p = witness.p
        else:
            x, y, p = witness
    except Exception:
        return [False] * 5

    # H1: x is an integer
    try:
        h1 = is_integer(x)
    except Exception:
        h1 = False

    # H2: y is an integer
    try:
        h2 = is_integer(y)
    except Exception:
        h2 = False

    # H3: x and y are coprime
    try:
        if h1 and h2:
            h3 = math.gcd(int(x), int(y)) == 1
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: p divides x^2 + y^2
    try:
        if is_integer(p) and int(p) != 0:
            h4 = (int(x)**2 + int(y)**2) % int(p) == 0
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: The prime p is congruent to 1 \pmod 4 (must FAIL, so we negate it)
    try:
        if is_integer(p):
            p_int = int(p)
            # The conclusion is that p is a prime AND p = 1 (mod 4)
            q = sympy.isprime(p_int) and (p_int % 4 == 1)
            neg_q = not q
        else:
            # If p is not an integer, it cannot be a prime congruent to 1 mod 4
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "H_2: y is an integer",
    "H_3: x and y are coprime",
    "H_4: p divides x^2 + y^2",
    "¬Q: p is not a prime congruent to 1 mod 4"
]

N_HYP = 4
NEG_Q_INDEX = 4