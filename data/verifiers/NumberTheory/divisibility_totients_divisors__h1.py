import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    If a divides b, then phi(a) divides phi(b).
    
    The true theorem requires a and b to be positive integers.
    Counterexamples typically involve zero or negative integers where the 
    totient function is undefined or behaves differently.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
        else:
            a, b = witness
            
        # Ensure we are working with integers, not floats
        if isinstance(a, float) or isinstance(b, float):
            return [False, False]
            
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False]

    # H_1: a divides b
    try:
        if a == 0:
            h1 = (b == 0)
        else:
            h1 = (b % a == 0)
    except Exception:
        h1 = False

    # Q: phi(a) divides phi(b)
    try:
        phi_a = sympy.totient(a)
        phi_b = sympy.totient(b)
        if phi_a == 0:
            q = (phi_b == 0)
        else:
            q = (phi_b % phi_a == 0)
    except Exception:
        # If totient is undefined (e.g., for n <= 0), the conclusion fails
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a divides b",
    "¬Q: \\phi(a) does not divide \\phi(b)"
]

N_HYP = 1
NEG_Q_INDEX = 1