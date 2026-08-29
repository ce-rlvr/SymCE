import math

def conditions(witness):
    """
    Given a witness (a, b, c), checks if it is a primitive Pythagorean triple
    with hypotenuse c, and evaluates whether the semiperimeter s and the 
    difference s-c are coprime integers.
    """
    try:
        # Witness should be a sequence of three numbers
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
        
        # Check if they are integers
        if not (int(a) == a and int(b) == b and int(c) == c):
            h1 = False
        else:
            a, b, c = int(a), int(b), int(c)
            is_pyth = (a**2 + b**2 == c**2)
            is_prim = (math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1)
            # c must be the hypotenuse (longest side, positive)
            is_hyp = (c > 0 and c >= abs(a) and c >= abs(b))
            h1 = is_pyth and is_prim and is_hyp
    except Exception:
        h1 = False

    try:
        a, b, c = witness
        if not (int(a) == a and int(b) == b and int(c) == c):
            concl = False
        else:
            a, b, c = int(a), int(b), int(c)
            # Semiperimeter s must be an integer
            if (a + b + c) % 2 != 0:
                concl = False
            else:
                s = (a + b + c) // 2
                s_c = s - c
                # Check if s and s-c are coprime
                concl = (math.gcd(abs(s), abs(s_c)) == 1)
    except Exception:
        concl = False

    # neg_Q is True when the conclusion FAILS (i.e., they are NOT coprime integers)
    return [bool(h1), not bool(concl)]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple with hypotenuse c",
    "¬Q: The semiperimeter s and the difference s-c are not coprime integers"
]

N_HYP = 1
NEG_Q_INDEX = 1