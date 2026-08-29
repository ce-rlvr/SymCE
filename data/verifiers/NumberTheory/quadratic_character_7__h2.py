import sympy

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    """
    try:
        p = int(witness)
    except Exception:
        return [False, False]

    # H_1: p is an odd prime
    try:
        h1_ok = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion fails at the witness.
    # The conclusion states: (7/p) = 1 iff p = +/-1, +/-3, +/-9 mod 28.
    # This implicitly assumes p does not divide 7 (so the symbol is +/- 1).
    # For p = 7, the Legendre symbol is 0, which violates the implicit dichotomy,
    # causing the characterization to fail.
    try:
        left = sympy.legendre_symbol(7, p)
        is_in_class = (p % 28 in [1, 3, 9, 19, 25, 27])
        
        if left == 0:
            # The conclusion fails because 0 is neither 1 nor -1.
            q = False
        else:
            q = (left == 1) == is_in_class
            
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: The characterization of (7/p) = 1 fails (e.g., symbol is 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1