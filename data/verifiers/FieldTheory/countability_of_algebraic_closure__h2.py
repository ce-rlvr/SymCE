import sympy
from sympy.polys.domains import QQ, RR, CC, ZZ, FF

# Setup
RealField = RR
ComplexField = CC
RationalField = QQ

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        F, K = witness
    else:
        F = witness
        K = None

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: K is the algebraic closure of F
    try:
        if K is not None:
            if F == RR and K == CC:
                h2 = True
            elif F == CC and K == CC:
                h2 = True
            else:
                h2 = False
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: K is not a countable set
    try:
        def is_uncountable(domain):
            if domain in (RR, CC):
                return True
            cls_name = type(domain).__name__
            if 'RealField' in cls_name or 'ComplexField' in cls_name:
                return True
            if str(domain) in ('RR', 'CC', 'RealField', 'ComplexField'):
                return True
            try:
                if hasattr(domain, 'domain') and domain.domain is not domain:
                    return is_uncountable(domain.domain)
            except Exception:
                pass
            return False
        
        if K is not None:
            neg_q = is_uncountable(K)
        else:
            neg_q = is_uncountable(F)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the algebraic closure of F",
    "¬Q: K is not a countable set"
]

N_HYP = 2
NEG_Q_INDEX = 2