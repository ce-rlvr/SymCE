import math

# Top-level setup
# No special named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: Let (a, b, c) be a primitive Pythagorean triple
    try:
        if len(witness) != 3:
            h1 = False
        else:
            a, b, c = witness
            # Check if they are integers
            if int(a) == a and int(b) == b and int(c) == c:
                a, b, c = int(a), int(b), int(c)
                if a > 0 and b > 0 and c > 0:
                    # A Pythagorean triple satisfies the Pythagorean theorem in some order
                    is_triple = (a**2 + b**2 == c**2) or (a**2 + c**2 == b**2) or (b**2 + c**2 == a**2)
                    # Primitive means gcd(a, b, c) == 1
                    is_primitive = math.gcd(math.gcd(a, b), c) == 1
                    h1 = is_triple and is_primitive
                else:
                    h1 = False
            else:
                h1 = False
    except Exception:
        h1 = False

    # neg_Q: The integers s-a and s-b are NOT coprime
    try:
        a, b, c = witness
        if int(a) == a and int(b) == b and int(c) == c:
            a, b, c = int(a), int(b), int(c)
            s_2 = a + b + c
            if s_2 % 2 != 0:
                neg_q = False
            else:
                s = s_2 // 2
                sa = s - a
                sb = s - b
                neg_q = math.gcd(sa, sb) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple",
    "¬Q: The integers s-a and s-b are not coprime"
]

N_HYP = 1
NEG_Q_INDEX = 1