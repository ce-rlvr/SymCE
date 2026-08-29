import math

def conditions(witness):
    try:
        h1 = False
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            if 'c' in witness:
                c = witness['c']
                if a == int(a) and b == int(b) and c == int(c) and a > 0 and b > 0 and c > 0:
                    a, b, c = int(a), int(b), int(c)
                    if a**2 + b**2 == c**2:
                        h1 = True
            else:
                if a == int(a) and b == int(b) and a > 0 and b > 0:
                    a, b = int(a), int(b)
                    c_sq = a**2 + b**2
                    c = int(math.isqrt(c_sq))
                    if c**2 == c_sq:
                        h1 = True
        else:
            if len(witness) == 2:
                a, b = witness[0], witness[1]
                if a == int(a) and b == int(b) and a > 0 and b > 0:
                    a, b = int(a), int(b)
                    c_sq = a**2 + b**2
                    c = int(math.isqrt(c_sq))
                    if c**2 == c_sq:
                        h1 = True
            elif len(witness) == 3:
                a, b, c = witness[0], witness[1], witness[2]
                if a == int(a) and b == int(b) and c == int(c) and a > 0 and b > 0 and c > 0:
                    a, b, c = int(a), int(b), int(c)
                    if a**2 + b**2 == c**2:
                        h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
        else:
            a, b = witness[0], witness[1]
            
        if a == int(a) and b == int(b):
            a, b = int(a), int(b)
            diff_mod_8 = abs(a - b) % 8
            if diff_mod_8 not in (1, 7):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are the legs of the triple",
    "¬Q: The absolute difference |a - b| is not congruent to either 1 modulo 8 or 7 modulo 8"
]

N_HYP = 1
NEG_Q_INDEX = 1