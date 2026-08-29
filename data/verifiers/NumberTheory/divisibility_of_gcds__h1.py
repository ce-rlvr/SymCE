import sympy

CONDITION_LABELS = [
    "H_1: a divides b",
    "H_2: c divides d",
    "¬Q: gcd(a, c) does not divide gcd(b, d)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def divides(x, y):
    if x == 0:
        return y == 0
    try:
        return (y % x) == 0
    except Exception:
        pass
    try:
        q, r = sympy.div(y, x)
        return r == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
        else:
            a, b, c, d = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = divides(a, b)
    except Exception:
        h1 = False
        
    try:
        h2 = divides(c, d)
    except Exception:
        h2 = False
        
    try:
        g1 = sympy.gcd(a, c)
        g2 = sympy.gcd(b, d)
        neg_q = not divides(g1, g2)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]