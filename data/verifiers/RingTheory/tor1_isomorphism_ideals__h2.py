import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (R, I, J), checks if it is a valid counterexample to the conjecture.
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'gens'):
            h1 = True
        elif R in (ZZ, QQ):
            h1 = True
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        h2 = False
        if isinstance(J, (list, tuple, set)):
            h2 = True
            for elem in J:
                if not (elem in R):
                    h2 = False
                    break
        elif hasattr(J, 'ring'):
            h2 = (J.ring == R)
    except Exception:
        h2 = False

    # ¬Q: Conclusion fails
    # The isomorphism Tor_1^R(R/I, R/J) ≅ (I ∩ J)/IJ is unconditionally true 
    # for any ideals I, J in a commutative ring R. 
    # The dropped hypothesis from the true theorem is "I is an ideal of R".
    # If I is not an ideal, the quotient R/I and the module structures are undefined 
    # or mathematically meaningless in this context, causing the conclusion to fail.
    try:
        is_ideal_I = False
        if isinstance(I, (list, tuple, set)):
            is_ideal_I = True
            for elem in I:
                if not (elem in R):
                    is_ideal_I = False
                    break
        elif hasattr(I, 'ring'):
            is_ideal_I = (I.ring == R)
            
        neg_q = not is_ideal_I
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: Tor_1^R(R/I, R/J) is not isomorphic to (I ∩ J)/IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2