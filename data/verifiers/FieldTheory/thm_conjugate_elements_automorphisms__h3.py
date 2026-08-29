import sympy
from sympy import minpoly

# Top-level setup for FieldTheory
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            F, E, alpha, beta = witness
        else:
            F = witness.F
            E = witness.E
            alpha = witness.alpha
            beta = witness.beta
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H_2: E is an algebraically closed field containing F
    try:
        h2 = False
        if getattr(E, 'is_Field', False):
            if E == sympy.CC:
                if F in [sympy.QQ, sympy.RR, sympy.CC]:
                    h2 = True
            elif getattr(E, 'is_algebraically_closed', False):
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The equivalence between sharing a minimal polynomial and being conjugate fails
    try:
        try:
            mp_alpha = minpoly(alpha, domain=F)
            alg_alpha = True
        except Exception:
            alg_alpha = False
            mp_alpha = None

        try:
            mp_beta = minpoly(beta, domain=F)
            alg_beta = True
        except Exception:
            alg_beta = False
            mp_beta = None

        if alg_alpha and alg_beta:
            share_minpoly = (mp_alpha == mp_beta)
            exists_auto = (mp_alpha == mp_beta)
        elif not alg_alpha and not alg_beta:
            # Neither has a minimal polynomial (transcendental over F), so they cannot share one.
            share_minpoly = False
            # By Steinitz's theorem, any two transcendental elements in an algebraically closed 
            # field of infinite transcendence degree (like CC over QQ) are conjugate.
            exists_auto = True
        else:
            share_minpoly = False
            exists_auto = False

        neg_q = not (share_minpoly == exists_auto)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraically closed field containing F",
    "¬Q: The equivalence between sharing a minimal polynomial and being conjugate fails"
]

N_HYP = 2
NEG_Q_INDEX = 2