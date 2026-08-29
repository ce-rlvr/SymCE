import sympy
from sympy.ntheory import totient
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness (an integer n) satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        # H_1: n is a positive integer (implying zeta_n is a primitive n-th root of unity)
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = (n >= 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 1:
                # The true degree of the maximal real subfield of Q(zeta_n) over Q
                # For n=1, Q(zeta_1) = Q, maximal real subfield is Q, degree 1
                # For n=2, Q(zeta_2) = Q, maximal real subfield is Q, degree 1
                # For n>=3, Q(zeta_n) is totally complex, maximal real subfield has degree phi(n)/2
                actual_degree = totient(n) if n <= 2 else totient(n) / 2
                
                # The conclusion claims the degree is always phi(n)/2
                claimed_degree = totient(n) / 2
                
                # The conclusion fails if the actual degree does not match the claimed degree
                neg_q = (actual_degree != claimed_degree)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (zeta_n is a primitive n-th root of unity)",
    "¬Q: The maximal real subfield does not have degree phi(n)/2 over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1