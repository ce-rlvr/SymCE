import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z
from sympy.polys.agca.ideals import Ideal
from sympy.polys.agca.modules import Module

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: There does not exist a surjective R-module homomorphism from I \\otimes_R J to IJ mapping x \\otimes y to xy"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            R = witness.R
            I = witness.I
            J = witness.J
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative is not None:
            h1 = bool(R.is_commutative)
    except Exception:
        pass

    # H2: I is an ideal of R
    h2 = False
    try:
        if isinstance(I, Ideal):
            h2 = (I.ring == R)
        elif hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal(R))
        elif callable(getattr(I, 'is_ideal_of', None)):
            h2 = bool(I.is_ideal_of(R))
    except Exception:
        pass

    # neg_Q: The conclusion fails.
    # The conclusion holds if J is an ideal of R (or an R-module over R).
    # It fails if J is not an R-module (e.g., a subring that is not an ideal).
    neg_q = False
    try:
        is_j_ideal_or_module = False
        if isinstance(J, Ideal):
            is_j_ideal_or_module = (J.ring == R)
        elif isinstance(J, Module):
            is_j_ideal_or_module = (J.ring == R)
        elif hasattr(J, 'is_ideal'):
            is_j_ideal_or_module = bool(J.is_ideal(R))
        elif callable(getattr(J, 'is_ideal_of', None)):
            is_j_ideal_or_module = bool(J.is_ideal_of(R))
        elif callable(getattr(J, 'is_module_over', None)):
            is_j_ideal_or_module = bool(J.is_module_over(R))
        
        neg_q = not is_j_ideal_or_module
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]