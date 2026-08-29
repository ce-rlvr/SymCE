import sympy
import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, b, d) of integers.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        a, b, d = witness
    except Exception:
        return [False, False, False, False]
        
    def is_int(x):
        return isinstance(x, (int, sympy.Integer))
        
    try:
        h1_ok = is_int(a) and is_int(b) and is_int(d)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = h1_ok and (a != 0) and (b != 0)
    except Exception:
        h2_ok = False
        
    try:
        h3_ok = h1_ok and (math.gcd(int(a), int(b)) == 1)
    except Exception:
        h3_ok = False
        
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            divs_a = sympy.divisors(int(a))
            divs_b = sympy.divisors(int(b))
            exists = False
            abs_d = abs(int(d))
            for x in divs_a:
                for y in divs_b:
                    if x * y == abs_d:
                        exists = True
                        break
                if exists:
                    break
            # The conclusion states that such d1, d2 exist (and are unique up to units).
            # In Z, uniqueness up to units is guaranteed if they exist, because gcd(a,b)=1.
            # Thus, the conclusion fails if and only if no such d1, d2 exist.
            neg_q_ok = not exists
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, d are elements of a UFD (Z)",
    "H_2: a and b are non-zero",
    "H_3: gcd(a, b) = 1",
    "¬Q: d cannot be factored into d1 * d2 where d1|a and d2|b"
]

N_HYP = 3
NEG_Q_INDEX = 3