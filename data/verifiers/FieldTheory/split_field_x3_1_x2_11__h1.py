import sympy
from sympy import Poly, factor, sqrt, I
from sympy.abc import x

def splits_completely(f, exts):
    try:
        factored = factor(f, extension=exts)
    except Exception:
        return None
        
    if factored.is_Mul:
        factors = factored.args
    else:
        factors = [factored]
        
    for fac in factors:
        if not fac.has(x):
            continue
        base, exp = fac.as_base_exp()
        try:
            if Poly(base, x).degree() != 1:
                return False
        except Exception:
            return None
    return True

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        pass

    try:
        p = Poly(witness, x, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            splits_all = splits_completely(witness, [sqrt(-3), sqrt(11)])
            if splits_all is None:
                neg_q = False
            elif not splits_all:
                neg_q = True
            else:
                splits_sub1 = splits_completely(witness, [sqrt(-3)])
                splits_sub2 = splits_completely(witness, [sqrt(11)])
                splits_sub3 = splits_completely(witness, [sqrt(-33)])
                
                if splits_sub1 is None or splits_sub2 is None or splits_sub3 is None:
                    neg_q = False
                elif splits_sub1 or splits_sub2 or splits_sub3:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the splitting field of f(x) over Q",
    "¬Q: K is not Q(sqrt(-3), sqrt(11)) or degree of K over Q is not 4"
]

N_HYP = 1
NEG_Q_INDEX = 1