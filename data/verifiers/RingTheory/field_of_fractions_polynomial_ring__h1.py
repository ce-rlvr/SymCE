import sympy
from sympy.abc import x

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    if isinstance(witness, dict):
        try:
            if 'h1' in witness and 'h2' in witness and 'neg_q' in witness:
                return [bool(witness['h1']), bool(witness['h2']), bool(witness['neg_q'])]
        except Exception:
            pass

    if hasattr(witness, 'h1') and hasattr(witness, 'h2') and hasattr(witness, 'neg_q'):
        try:
            return [bool(witness.h1()), bool(witness.h2()), bool(witness.neg_q())]
        except Exception:
            pass

    try:
        if hasattr(witness, 'R'):
            R = witness.R
            K = witness.K
            R_x = witness.R_x
        elif isinstance(witness, tuple) and len(witness) >= 3:
            R, K, R_x = witness[:3]
        else:
            R = witness
            K = R.frac_field()
            R_x = R.poly_ring(x)
    except Exception:
        return [False, False, False]

    try:
        h1_ok = (K == R.frac_field())
    except Exception:
        h1_ok = False

    try:
        h2_ok = (R_x == R.poly_ring(x))
    except Exception:
        h2_ok = False

    try:
        K_x = K.poly_ring(x).frac_field()
        try:
            F_Rx = R_x.frac_field()
            neg_q_ok = (F_Rx != K_x)
        except Exception:
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: The polynomial ring is in one variable over R",
    "¬Q: The field of fractions of the polynomial ring is not isomorphic to K(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2