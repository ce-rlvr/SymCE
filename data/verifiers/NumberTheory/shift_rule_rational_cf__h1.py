import sympy
from sympy import Rational

def eval_cf(cf):
    if not cf:
        return None
    try:
        res = Rational(int(cf[-1]), 1)
        for x in reversed(cf[:-1]):
            if res == 0:
                return None
            res = int(x) + 1 / res
        return res
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        a, b, cf = witness
        a = int(a)
        b = int(b)
        
        if b == 0:
            h1 = False
        elif not isinstance(cf, list) or len(cf) == 0:
            h1 = False
        else:
            is_valid_cf = True
            for x in cf:
                try:
                    if int(x) != x or isinstance(x, bool):
                        is_valid_cf = False
                        break
                except Exception:
                    is_valid_cf = False
                    break
            
            if not is_valid_cf:
                h1 = False
            elif len(cf) > 1 and not all(int(x) >= 1 for x in cf[1:]):
                h1 = False
            else:
                val = eval_cf(cf)
                h1 = (val == Rational(a, b))
    except Exception:
        h1 = False

    try:
        a, b, cf = witness
        a = int(a)
        b = int(b)
        
        mod = a % b
        if mod == 0:
            q = False
        else:
            target = Rational(b, mod)
            cf_tail = cf[1:]
            if not cf_tail:
                q = False
            else:
                val = eval_cf(cf_tail)
                q = (val == target)
    except Exception:
        q = False

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: The rational number a/b has the finite simple continued fraction expansion cf",
    "¬Q: The simple continued fraction expansion of b / (a mod b) is NOT given by the tail of cf"
]

N_HYP = 1
NEG_Q_INDEX = 1