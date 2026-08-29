import sympy
from sympy import ZZ, QQ

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localization S^{-1}R is not a Euclidean domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Euclidean domain
    h1 = False
    try:
        if R == ZZ:
            h1 = True
        elif getattr(R, 'is_Field', False):
            h1 = True
        elif hasattr(R, 'domain') and getattr(R.domain, 'is_Field', False):
            if hasattr(R, 'symbols') and len(R.symbols) == 1:
                h1 = True
            elif hasattr(R, 'gens') and len(R.gens) == 1:
                h1 = True
    except Exception:
        pass

    # H_2: S is a multiplicatively closed subset of R
    h2 = False
    try:
        if hasattr(S, '__iter__'):
            S_list = list(S)
            if len(S_list) <= 1000:  # reasonable size limit for evaluation
                subset_ok = True
                for s in S_list:
                    if s not in R:
                        subset_ok = False
                        break
                
                if subset_ok:
                    # Standard definition requires 1 in S
                    has_one = (R.one in S_list)
                    
                    # Check closure under multiplication
                    closed = True
                    for a in S_list:
                        for b in S_list:
                            if R.mul(a, b) not in S_list:
                                closed = False
                                break
                        if not closed:
                            break
                    
                    if has_one and closed:
                        h2 = True
    except Exception:
        pass

    # ¬Q: The localization S^{-1}R is not a Euclidean domain
    # If R is a Euclidean domain and 0 \notin S, S^{-1}R is ALWAYS a Euclidean domain.
    # The only way S^{-1}R fails to be a Euclidean domain is if 0 \in S,
    # in which case S^{-1}R is the zero ring (which is not an integral domain, hence not Euclidean).
    neg_q = False
    try:
        if hasattr(S, '__iter__'):
            S_list = list(S)
            if R.zero in S_list:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]