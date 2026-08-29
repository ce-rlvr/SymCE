import sympy

# Top-level setup
# No named bindings needed for this Number Theory conjecture; use integers directly.

def conditions(witness) -> list[bool]:
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: Let a be an integer such that 1 < a < p
    try:
        h1 = (int(a) == a) and (1 < a < p)
    except Exception:
        h1 = False
        
    # H2: Assume a divides p + 1
    try:
        h2 = ((p + 1) % a == 0)
    except Exception:
        h2 = False
        
    # Q: The modular inverse of a modulo p is congruent to (p+1)/a (mod p)
    try:
        a_int = int(a)
        p_int = int(p)
        
        # Compute the modular inverse of a modulo p
        inv_a = pow(a_int, -1, p_int)
        
        # Compute the expected value (p+1)/a modulo p
        expected = ((p_int + 1) // a_int) % p_int
        
        q = (inv_a == expected)
        neg_q = not q
    except Exception:
        # If modular inverse doesn't exist or another error occurs, the conclusion fails
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer such that 1 < a < p",
    "H_2: a divides p + 1",
    "¬Q: The modular inverse of a modulo p is NOT congruent to (p+1)/a (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2