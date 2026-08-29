import sympy
from sympy.polys.domains import QQ, RR, CC, ZZ
from sympy import sqrt, I

def conditions(witness):
    """
    Check the hypotheses and negated conclusion for the false conjecture:
    "Every algebraic extension of a field is algebraically closed."
    
    The witness should be a tuple (F, E) where F and E are sympy domains
    (e.g., (QQ, QQ.algebraic_field(sqrt(2)))).
    """
    try:
        F, E = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: E is an extension field of F
    try:
        h2 = False
        if getattr(E, 'is_Field', False):
            if F == E:
                h2 = True
            elif F == QQ:
                if E in (QQ, RR, CC) or getattr(E, 'is_AlgebraicField', False):
                    h2 = True
            elif F == RR:
                if E in (RR, CC):
                    h2 = True
            elif hasattr(F, 'order') and hasattr(E, 'order') and hasattr(F, 'characteristic') and hasattr(E, 'characteristic'):
                if (E.order - 1) % (F.order - 1) == 0 and F.characteristic() == E.characteristic():
                    h2 = True
    except Exception:
        h2 = False

    # H_3: E is an algebraic extension of F
    try:
        h3 = False
        if h2:
            if F == E:
                h3 = True
            elif F == QQ and getattr(E, 'is_AlgebraicField', False):
                h3 = True
            elif F == RR and E == CC:
                h3 = True
            elif hasattr(F, 'order') and hasattr(E, 'order') and hasattr(F, 'characteristic') and hasattr(E, 'characteristic'):
                if (E.order - 1) % (F.order - 1) == 0 and F.characteristic() == E.characteristic():
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: E is not an algebraically closed field
    # In sympy, CC is the only algebraically closed field domain.
    try:
        neg_q = (E != CC)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: E is an algebraic extension of F",
    "¬Q: E is not an algebraically closed field"
]

N_HYP = 3
NEG_Q_INDEX = 3