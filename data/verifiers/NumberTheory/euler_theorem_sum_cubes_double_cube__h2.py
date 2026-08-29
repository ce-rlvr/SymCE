import sympy

CONDITION_LABELS = [
    "H_1: x, y, z are integers",
    "¬Q: It is not the case that (x = y = z or (x = -y and z = 0))"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        x, y, z = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(x, (int, sympy.Integer)) and \
             isinstance(y, (int, sympy.Integer)) and \
             isinstance(z, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    try:
        q = (x == y and y == z) or (x == -y and z == 0)
        neg_q = bool(not q)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]