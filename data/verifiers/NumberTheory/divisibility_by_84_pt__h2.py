import sympy

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c)):
            if a > 0 and b > 0 and c > 0:
                h1 = True
    except Exception:
        h1 = False
        
    try:
        val = int(a) * int(b) * (int(a)**2 - int(b)**2)
        neg_q = (val % 84) != 0
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "¬Q: ab(a^2 - b^2) is not divisible by 84"
]

N_HYP = 1
NEG_Q_INDEX = 1