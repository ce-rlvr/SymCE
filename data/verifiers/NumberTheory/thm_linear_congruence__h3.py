import math

CONDITION_LABELS = [
    "H_1: a, b, and m are integers",
    "H_2: m > 0",
    "¬Q: The linear congruence ax ≡ b (mod m) has a solution iff d divides b fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            m = witness.get('m')
            d = witness.get('d')
            if any(x is None for x in (a, b, m, d)):
                return [False, False, False]
        elif hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'm') and hasattr(witness, 'd'):
            a = witness.a
            b = witness.b
            m = witness.m
            d = witness.d
        else:
            a, b, m, d = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and m are integers
    try:
        h1 = type(a) is int and type(b) is int and type(m) is int
    except Exception:
        h1 = False

    # H_2: m > 0
    try:
        h2 = type(m) is int and m > 0
    except Exception:
        h2 = False

    # ¬Q: The linear congruence ax ≡ b (mod m) has a solution iff d divides b
    try:
        if type(d) is not int:
            neg_q = False
        else:
            has_solution = (b % math.gcd(a, m) == 0)
            if d == 0:
                d_divides_b = (b == 0)
            else:
                d_divides_b = (b % d == 0)
            
            q = (has_solution == d_divides_b)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]