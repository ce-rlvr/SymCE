import sympy
from sympy import sympify
from sympy.ntheory.continued_fraction import continued_fraction_iterator

def compare_minkowski_q(x, y, max_terms=1000):
    if x == y:
        return False
    
    cf_x = continued_fraction_iterator(x)
    cf_y = continued_fraction_iterator(y)
    
    try:
        a0 = next(cf_x)
    except StopIteration:
        a0 = 0
    try:
        b0 = next(cf_y)
    except StopIteration:
        b0 = 0
        
    if a0 != b0:
        return bool(a0 < b0)
        
    k = 1
    while k < max_terms:
        try:
            a = next(cf_x)
        except StopIteration:
            a = float('inf')
        try:
            b = next(cf_y)
        except StopIteration:
            b = float('inf')
            
        if a != b:
            if k % 2 == 1:
                return bool(a > b)
            else:
                return bool(a < b)
                
        if a == float('inf') and b == float('inf'):
            return False
            
        k += 1
        
    return bool(x.evalf(100) < y.evalf(100))

def conditions(witness):
    try:
        w_list = list(witness)
        if len(w_list) != 2:
            return [False] * 6
        x, y = sympify(w_list[0]), sympify(w_list[1])
    except Exception:
        return [False] * 6

    try:
        h1 = bool(x.is_irrational == True)
    except Exception:
        h1 = False

    try:
        h2 = bool(y.is_irrational == True)
    except Exception:
        h2 = False

    try:
        h3 = bool(x >= 0 and x <= 1)
    except Exception:
        h3 = False

    try:
        h4 = bool(y >= 0 and y <= 1)
    except Exception:
        h4 = False

    try:
        h5 = bool(x < y)
    except Exception:
        h5 = False

    try:
        q_less = compare_minkowski_q(x, y)
        neg_q = not q_less
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: x is irrational",
    "H_2: y is irrational",
    "H_3: x is between 0 and 1",
    "H_4: y is between 0 and 1",
    "H_5: x < y",
    "¬Q: Q(x) >= Q(y)"
]

N_HYP = 5
NEG_Q_INDEX = 5