import sympy
from sympy import Poly, factor_list, sqrt
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a polynomial f(x).
    """
    # H_1: f(x) is a polynomial over Q
    h1_ok = False
    try:
        p = Poly(witness, x)
        h1_ok = all(c.is_Rational for c in p.coeffs())
    except Exception:
        h1_ok = False

    # neg_Q: The splitting field of f is NOT Q(sqrt(-3)) OR its degree over Q is NOT 2
    neg_q_ok = False
    try:
        def splits_completely(f, ext=None):
            if ext is None:
                factors = factor_list(f)[1]
            else:
                factors = factor_list(f, extension=ext)[1]
            return all(Poly(fac, x).degree() == 1 for fac, mult in factors)

        # The splitting field of f is Q(sqrt(-3)) and has degree 2 over Q
        # if and only if f splits completely over Q(sqrt(-3)) but does NOT split completely over Q.
        splits_Q = splits_completely(witness)
        splits_Q_sqrt_minus_3 = splits_completely(witness, ext=sqrt(-3))
        
        conclusion_holds = splits_Q_sqrt_minus_3 and not splits_Q
        neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The splitting field of f is not Q(sqrt(-3)) or its degree over Q is not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1