import sympy
from sympy.ntheory import factorint

def conditions(witness):
    try:
        # Check if witness is a positive integer
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and witness >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            if n == 1:
                sols = 1
                r = 0
            else:
                factors = factorint(n)
                r = len(factors)
                
                # Calculate the number of solutions to x^2 = 1 mod n
                # using the Chinese Remainder Theorem.
                sols = 1
                for p, e in factors.items():
                    if p == 2:
                        if e == 1:
                            sols *= 1
                        elif e == 2:
                            sols *= 2
                        else:
                            sols *= 4
                    else:
                        sols *= 2
            
            # The conclusion states there are exactly 2^r solutions.
            # neg_q is True if this conclusion FAILS.
            neg_q = bool(sols != 2**r)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The congruence x^2 ≡ 1 (mod n) does not have exactly 2^r distinct solutions"
]

N_HYP = 1
NEG_Q_INDEX = 1