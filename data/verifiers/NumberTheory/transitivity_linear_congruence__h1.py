import sympy

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "H_2: a == b (mod m)",
    "H_3: b == c (mod m)",
    "¬Q: a != c (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_int(x):
    if isinstance(x, int) or isinstance(x, sympy.Integer):
        return True
    if hasattr(x, 'is_integer') and x.is_integer:
        return True
    return False

def is_congruent(x, y, m):
    if m == 0:
        return x == y
    try:
        if (x - y) % m == 0:
            return True
    except Exception:
        pass
    try:
        if sympy.Mod(x - y, m) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            m = witness['m']
        else:
            a, b, c, m = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(is_int(a) and is_int(b) and is_int(c))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_congruent(a, b, m))
    except Exception:
        h2 = False
        
    try:
        h3 = bool(is_congruent(b, c, m))
    except Exception:
        h3 = False
        
    try:
        neg_q = not bool(is_congruent(a, c, m))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]