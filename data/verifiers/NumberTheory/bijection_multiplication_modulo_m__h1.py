import sympy

def is_int(val):
    if isinstance(val, int):
        return True
    if hasattr(val, 'is_integer'):
        if callable(val.is_integer):
            return val.is_integer()
        else:
            return bool(val.is_integer)
    return False

def conditions(witness):
    try:
        a, m = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_int(a)
    except Exception:
        h1 = False
        
    try:
        h2 = sympy.gcd(a, m) == 1
    except Exception:
        h2 = False
        
    try:
        if not is_int(m) or not is_int(a):
            neg_q = True
        else:
            m_int = int(m)
            a_int = int(a)
            if m_int == 0:
                # Modulo 0 is undefined in standard programming and does not form 
                # a finite set of congruence classes in the context of this theorem.
                neg_q = True
            else:
                # For non-zero integers, the mapping f(x) = ax mod m is a bijection 
                # on Z/mZ if and only if a and m are coprime.
                neg_q = sympy.gcd(a_int, m_int) != 1
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: gcd(a, m) = 1",
    "¬Q: The mapping f(x) = ax mod m is not a bijection on the set of congruence classes modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2