import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S_set = witness.get('S')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            R, S_set = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring and getattr(R, 'is_commutative', False):
            h1 = True
        elif R in (ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        elif type(R).__name__ in ('PolynomialRing', 'FractionField'):
            h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if h1:
            h2 = True
    except Exception:
        pass

    neg_q = False
    try:
        if not hasattr(S_set, '__iter__'):
            neg_q = False
        else:
            S_list = list(S_set)
            if len(S_list) == 0:
                neg_q = True
            else:
                is_mult_closed = True
                for a in S_list:
                    try:
                        if hasattr(R, '__contains__') and a not in R:
                            is_mult_closed = False
                            break
                    except Exception:
                        pass
                    
                    for b in S_list:
                        try:
                            if hasattr(R, 'mul'):
                                prod = R.mul(a, b)
                            else:
                                prod = a * b
                        except Exception:
                            is_mult_closed = False
                            break
                        
                        found = False
                        for s in S_list:
                            if prod == s:
                                found = True
                                break
                        if not found:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
                neg_q = not is_mult_closed
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2