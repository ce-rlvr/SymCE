import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: There does not exist a surjective R-module homomorphism from I \\otimes_R J to IJ mapping x \\otimes y to xy"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (R, I, J), checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis was "I is an ideal of R".
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R in (QQ, ZZ, sympy.S.Integers, sympy.S.Rationals):
            h1 = True
        elif hasattr(R, 'is_Ring') and getattr(R, 'is_Ring', False) and getattr(R, 'is_commutative', False):
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        h2 = False
        if hasattr(J, 'ring') and J.ring == R:
            h2 = True
        elif J == R:
            h2 = True
        elif hasattr(J, 'is_Ideal') and getattr(J, 'is_Ideal', False) and getattr(J, 'ring', None) == R:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # The conclusion holds iff I is an R-module (which makes the tensor product well-defined).
    # If I is not an R-module, I \otimes_R J is undefined, so the homomorphism cannot exist.
    try:
        is_r_mod = False
        if hasattr(I, 'ring') and I.ring == R:
            is_r_mod = True
        elif I == R:
            is_r_mod = True
        elif hasattr(I, 'unify'):
            try:
                # In sympy domains, if R is a subring of I, I.unify(R) == I
                # This implies I is an R-algebra, hence an R-module.
                if I.unify(R) == I:
                    is_r_mod = True
            except Exception:
                pass
        
        neg_q = not is_r_mod
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]