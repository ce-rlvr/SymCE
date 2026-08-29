import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            p = witness.get('p')
        elif hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'p'):
            a = getattr(witness, 'a')
            b = getattr(witness, 'b')
            p = getattr(witness, 'p')
        else:
            a, b, p = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and p are integers
    try:
        h1 = False
        if not (isinstance(a, bool) or isinstance(b, bool) or isinstance(p, bool)):
            if int(a) == a and int(b) == b and int(p) == p:
                h1 = True
    except Exception:
        h1 = False

    # H_2: p does not divide a
    try:
        if p == 0:
            h2 = False
        else:
            h2 = (a % p != 0)
    except Exception:
        h2 = False

    # ¬Q: ax ≡ b (mod p) does not have exactly one solution modulo p
    try:
        if p == 0:
            neg_q = False
        else:
            a_int = int(a)
            b_int = int(b)
            p_int = abs(int(p))
            
            # The number of solutions to ax ≡ b (mod p) is gcd(a, p) if gcd(a, p) divides b, else 0.
            g = math.gcd(a_int, p_int)
            if b_int % g == 0:
                solutions = g
            else:
                solutions = 0
                
            neg_q = (solutions != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and p are integers",
    "H_2: p does not divide a",
    "¬Q: The linear congruence ax ≡ b (mod p) does not have exactly one solution modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2