import sympy
from sympy import ZZ, QQ
from sympy.polys.domains.polynomialring import PolynomialRing
from sympy.polys.domains.fractionfield import FractionField
from sympy.polys.agca.ideals import Ideal

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
        else:
            R, I = witness
    except Exception:
        return [False, False]

    # H1: R is a commutative Noetherian ring
    def is_commutative_noetherian(ring):
        if ring in (ZZ, QQ):
            return True
        if isinstance(ring, PolynomialRing) and is_commutative_noetherian(ring.domain):
            return True
        if isinstance(ring, FractionField) and is_commutative_noetherian(ring.domain):
            return True
        return False

    try:
        h1 = is_commutative_noetherian(R)
    except Exception:
        h1 = False

    # neg_Q: I cannot be expressed as the intersection of a finite number of primary ideals.
    # In a commutative Noetherian ring, every ideal has a primary decomposition (Lasker-Noether).
    # Thus, I can be expressed as such an intersection iff I is an ideal of R.
    # We check if I is an ideal. If it is NOT an ideal, then neg_Q is True.
    try:
        if isinstance(I, Ideal):
            neg_q = False
        elif isinstance(I, (list, set, tuple)) or isinstance(I, sympy.sets.Set):
            try:
                # A finite subset is an ideal iff it is exactly {0}
                if len(I) > 0:
                    is_zero = True
                    for x in I:
                        try:
                            if x != 0 and x != R.zero:
                                is_zero = False
                                break
                        except Exception:
                            if x != 0:
                                is_zero = False
                                break
                    if is_zero:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    neg_q = True
            except Exception:
                # If we can't determine its length or iterate, assume it's not an ideal
                neg_q = True
        elif I == R:
            # The whole ring is an ideal (the improper ideal)
            neg_q = False
        else:
            # Otherwise, assume it's not an ideal
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: I cannot be expressed as the intersection of a finite number of primary ideals"
]
N_HYP = 1
NEG_Q_INDEX = 1