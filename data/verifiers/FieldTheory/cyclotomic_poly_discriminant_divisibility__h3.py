import sympy as sp

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    The witness can be an integer `n` or a tuple `(n, P)`.
    """
    x = sp.Symbol('x')
    
    # Parse witness
    if isinstance(witness, tuple):
        if len(witness) == 2:
            n, P_wit = witness
        else:
            n = witness[0]
            P_wit = None
    else:
        n = witness
        P_wit = None

    # H_1: n >= 1 is an integer
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H_2: \Phi_n(x) is the n-th cyclotomic polynomial over \mathbb{Q}
    try:
        P_true = sp.cyclotomic_poly(n, x)
        if P_wit is not None:
            h2 = bool(P_wit == P_true)
            P = P_wit
        else:
            h2 = True
            P = P_true
    except Exception:
        h2 = False
        P = None

    # ¬Q: \Delta(\Phi_n) does NOT divide n^{\phi(n)} in \mathbb{Z}
    try:
        if P is None:
            neg_q = False
        else:
            D = sp.discriminant(P, x)
            val = n**sp.totient(n)
            if D == 0:
                neg_q = (val != 0)
            else:
                neg_q = (val % D != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial over Q",
    "¬Q: The discriminant of Phi_n(x) does not divide n^phi(n) in Z"
]

N_HYP = 2
NEG_Q_INDEX = 2