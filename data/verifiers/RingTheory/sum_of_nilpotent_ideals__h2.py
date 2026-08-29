import sympy
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def eq(a, b):
    try:
        res = (a == b)
        if isinstance(res, bool):
            if res: return True
        else:
            if bool(res): return True
    except Exception:
        pass
    try:
        diff = a - b
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        res = (diff == 0)
        if isinstance(res, bool):
            if res: return True
        else:
            if bool(res): return True
    except Exception:
        pass
    return False

def is_zero(x):
    try:
        if hasattr(x, 'is_zero_matrix') and x.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(x, 'is_zero') and x.is_zero:
            return True
    except Exception:
        pass
    try:
        res = (x == 0)
        if isinstance(res, bool):
            if res: return True
        else:
            if bool(res): return True
    except Exception:
        pass
    try:
        _ = iter(x)
        if all(eq(e, 0) for e in x):
            return True
    except Exception:
        pass
    return False

def is_ring(R):
    try:
        R_list = list(R)
    except Exception:
        return False
    if not R_list: return False
    
    zeros_list = [x for x in R_list if is_zero(x)]
    if not zeros_list: return False
    z = zeros_list[0]
    
    def contains(x):
        return any(eq(x, r) for r in R_list)
        
    for a in R_list:
        if not any(eq(a + b, z) for b in R_list):
            return False
        for b in R_list:
            if not contains(a + b): return False
            if not contains(a * b): return False
            
    n = len(R_list)
    if n <= 20:
        for a in R_list:
            for b in R_list:
                for c in R_list:
                    if not eq((a + b) + c, a + (b + c)): return False
                    if not eq((a * b) * c, a * (b * c)): return False
                    if not eq(a * (b + c), (a * b) + (a * c)): return False
                    if not eq((a + b) * c, (a * c) + (b * c)): return False
                    
    return True

def is_ideal(S, R):
    try:
        S_list = list(S)
        R_list = list(R)
    except Exception:
        return False
    if not S_list: return False
    
    def contains_S(x):
        return any(eq(x, s) for s in S_list)
        
    def contains_R(x):
        return any(eq(x, r) for r in R_list)
        
    for s in S_list:
        if not contains_R(s): return False
        
    for a in S_list:
        for b in S_list:
            if not contains_S(a + b): return False
            
    for s in S_list:
        for r in R_list:
            if not contains_S(r * s): return False
            if not contains_S(s * r): return False
            
    if not any(is_zero(s) for s in S_list): return False
    
    zeros_list = [x for x in S_list if is_zero(x)]
    if zeros_list:
        z = zeros_list[0]
        for s in S_list:
            if not any(eq(s + b, z) for b in S_list): return False
            
    return True

def is_nilpotent(S, R):
    try:
        S_list = list(S)
        R_list = list(R)
    except Exception:
        return False
    if not S_list: return True
    
    current_power = S_list
    for _ in range(len(R_list) + 1):
        if all(is_zero(x) for x in current_power):
            return True
        
        next_power = []
        for a in current_power:
            for b in S_list:
                prod = a * b
                if not any(eq(prod, x) for x in next_power):
                    next_power.append(prod)
        current_power = next_power
        
    return False

def get_sum(I, J):
    I_list = list(I)
    J_list = list(J)
    res = []
    for i in I_list:
        for j in J_list:
            s = i + j
            if not any(eq(s, x) for x in res):
                res.append(s)
    return res

def conditions(witness):
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(J, R) and is_nilpotent(J, R)
    except Exception:
        h2 = False
        
    try:
        I_plus_J = get_sum(I, J)
        q = is_ideal(I_plus_J, R) and is_nilpotent(I_plus_J, R)
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: J is a nilpotent ideal of R",
    "¬Q: The sum ideal I + J is NOT a nilpotent ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2