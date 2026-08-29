import sympy
from sympy import Poly, QQ, ZZ, Rational
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a field",
    "not Q: Factor ring is not a principal ideal ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, f = witness
        elif hasattr(witness, 'domain'):
            F = witness.domain
            f = witness
        else:
            F = witness
            f = x
            
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, f = witness
        elif hasattr(witness, 'domain'):
            F = witness.domain
            f = witness
        else:
            F = witness
            f = x

        # If F is a field, F[x] is a Principal Ideal Domain (PID).
        # The quotient of a PID by any ideal is always a Principal Ideal Ring (PIR).
        if getattr(F, 'is_Field', False):
            is_pir = True
        else:
            # If F is not a field, e.g., F = ZZ
            if F == ZZ:
                try:
                    f_poly = Poly(f, x)
                    if f_poly.is_zero:
                        is_pir = False # ZZ[x] is not a PIR
                    elif f_poly.degree() == 1 and f_poly.LC() in [1, -1]:
                        is_pir = True # ZZ[x]/(x-a) is isomorphic to ZZ, which is a PIR
                    else:
                        # For other polynomials over ZZ, the quotient is generally not a PIR
                        is_pir = False
                except Exception:
                    is_pir = False
            else:
                is_pir = False
                
        neg_q = not is_pir
    except Exception:
        neg_q = False

    return [h1, neg_q]