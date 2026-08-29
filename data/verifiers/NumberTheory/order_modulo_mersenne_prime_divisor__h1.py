import sympy
import sympy.ntheory

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (p, q), checks if it is a valid counterexample to the conjecture.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        p, q = witness
    except Exception:
        return [False, False, False, False]

    # H_1: M_p = 2^p - 1 (Implicitly requires p to be a positive integer)
    try:
        h1 = (int(p) == p) and (p > 0)
    except Exception:
        h1 = False

    # H_2: q is a prime number
    try:
        h2 = bool(sympy.isprime(q))
    except Exception:
        h2 = False

    # H_3: q divides M_p
    try:
        if h1 and (int(q) == q) and (q > 1):
            h3 = (pow(2, int(p), int(q)) == 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The multiplicative order of 2 modulo q is not p
    try:
        if h2 and h3:
            # Since q is prime and divides 2^p - 1 (which is odd for p > 0), 
            # q is an odd prime, so gcd(2, q) == 1 and n_order is well-defined.
            order = sympy.ntheory.n_order(2, int(q))
            neg_q = (order != int(p))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M_p = 2^p - 1",
    "H_2: q is a prime number",
    "H_3: q divides M_p",
    "¬Q: The multiplicative order of 2 modulo q is not p"
]

N_HYP = 3
NEG_Q_INDEX = 3