import math

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness can be a tuple (n, a, b) or (n, a, b, a_inv, b_inv), or a dictionary.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            b = witness.get('b')
            a_inv = witness.get('a_inv')
            b_inv = witness.get('b_inv')
        else:
            n = witness[0]
            a = witness[1]
            b = witness[2]
            a_inv = witness[3] if len(witness) > 3 else None
            b_inv = witness[4] if len(witness) > 4 else None
            
        n = int(n)
        a = int(a)
        b = int(b)
        if a_inv is not None: 
            a_inv = int(a_inv)
        if b_inv is not None: 
            b_inv = int(b_inv)
    except Exception:
        return [False, False, False]

    # H_1: Let n be an integer with n > 1
    try:
        h1_ok = bool(n > 1)
    except Exception:
        h1_ok = False

    # H_2: Let a^-1 and b^-1 denote the modular inverses of a and b modulo n, respectively.
    # In formal systems, if the coprime hypothesis is dropped, the inverse function is typically 
    # totalized (e.g., returning 0 when gcd != 1). We allow the witness to provide these totalized 
    # values, or we compute them using the standard totalization (0 for non-coprime).
    try:
        h2_ok = True
        if a_inv is not None:
            # If provided, it must be a valid inverse when coprime
            if math.gcd(a, n) == 1 and (a * a_inv) % n != 1:
                h2_ok = False
        else:
            a_inv = pow(a, -1, n) if math.gcd(a, n) == 1 else 0
            
        if b_inv is not None:
            if math.gcd(b, n) == 1 and (b * b_inv) % n != 1:
                h2_ok = False
        else:
            b_inv = pow(b, -1, n) if math.gcd(b, n) == 1 else 0
    except Exception:
        h2_ok = False

    # Q: The difference a^-1 - b^-1 is congruent to b^-1 a^-1 (b - a) (mod n)
    try:
        left = (a_inv - b_inv) % n
        right = (b_inv * a_inv * (b - a)) % n
        q_ok = (left == right)
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer with n > 1",
    "H_2: Let a^-1 and b^-1 denote the modular inverses of a and b modulo n, respectively",
    "¬Q: The difference a^-1 - b^-1 is not congruent to b^-1 a^-1 (b - a) modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2