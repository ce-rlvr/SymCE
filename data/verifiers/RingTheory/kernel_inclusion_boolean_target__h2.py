import sympy
from sympy import ZZ, QQ

class ZnRing:
    def __init__(self, n):
        self.n = n
        self.is_ring = True
        self.is_commutative = True
        self.has_Identity = True
        self.one = 1
        self.zero = 0
        self.elements = list(range(n))
        
    def add(self, x, y): 
        return (x + y) % self.n
        
    def mul(self, x, y): 
        return (x * y) % self.n
        
    def neg(self, x): 
        return (-x) % self.n
        
    def __str__(self): 
        return f"Z_{self.n}"
        
    def __repr__(self): 
        return f"Z_{self.n}"

# Top-level setup: named object bindings that the witness expression may reference
Z2 = ZnRing(2)
Z3 = ZnRing(3)
Z4 = ZnRing(4)
Z5 = ZnRing(5)
Z6 = ZnRing(6)

def is_ring(add, mul):
    n = len(add)
    if any(len(row) != n for row in add) or len(mul) != n or any(len(row) != n for row in mul):
        return False
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
    return True

def is_commutative(mul):
    n = len(mul)
    for i in range(n):
        for j in range(n):
            if mul[i][j] != mul[j][i]: return False
    return True

def get_identity(mul):
    n = len(mul)
    for i in range(n):
        if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
            return i
    return -1

def get_test_elements(domain):
    if hasattr(domain, 'elements'):
        return list(domain.elements)
    if domain in (ZZ, QQ):
        return list(range(-10, 11))
    if hasattr(domain, 'characteristic'):
        p = domain.characteristic
        if callable(p):
            p = p()
        if p > 0:
            return [domain(i) for i in range(p)]
    return list(range(-10, 11))

def apply_f(f, x):
    if isinstance(f, (dict, list, tuple)):
        return f[x]
    return f(x)

def check_dict_format(witness):
    try:
        R_add = witness['R_add']
        R_mul = witness['R_mul']
        B_add = witness['B_add']
        B_mul = witness['B_mul']
        f = witness['f']
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R_add, R_mul) and is_commutative(R_mul) and get_identity(R_mul) != -1
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring(B_add, B_mul)
        n = len(R_add)
        m = len(B_add)
        if len(f) != n: h2 = False
        for i in range(n):
            if not (0 <= f[i] < m): h2 = False
        if h2:
            for i in range(n):
                for j in range(n):
                    if f[R_add[i][j]] != B_add[f[i]][f[j]]: h2 = False
                    if f[R_mul[i][j]] != B_mul[f[i]][f[j]]: h2 = False
            id_R = get_identity(R_mul)
            id_B = get_identity(B_mul)
            if id_B != -1 and f[id_R] != id_B:
                h2 = False
    except Exception:
        h2 = False
        
    try:
        n = len(R_add)
        m = len(B_add)
        B_zero = -1
        for i in range(m):
            if all(B_add[i][j] == j for j in range(m)):
                B_zero = i
                break
        R_zero = -1
        for i in range(n):
            if all(R_add[i][j] == j for j in range(n)):
                R_zero = i
                break
        R_neg = [-1]*n
        for i in range(n):
            for j in range(n):
                if R_add[i][j] == R_zero:
                    R_neg[i] = j
                    break
        
        neg_q = False
        for x in range(n):
            x2 = R_mul[x][x]
            minus_x = R_neg[x]
            val = R_add[x2][minus_x]
            if f[val] != B_zero:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

def check_tuple_format(witness):
    try:
        R, B, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = False
        if hasattr(R, 'is_ring') and R.is_ring and hasattr(R, 'is_commutative') and R.is_commutative:
            if hasattr(R, 'has_Identity') and R.has_Identity:
                h1 = True
            elif hasattr(R, 'one'):
                h1 = True
        elif R in (ZZ, QQ):
            h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = True
        if not (hasattr(B, 'is_ring') and B.is_ring) and B not in (ZZ, QQ):
            h2 = False
            
        test_R = get_test_elements(R)
        
        for x in test_R:
            for y in test_R:
                if hasattr(R, 'add') and hasattr(R, 'mul'):
                    x_plus_y = R.add(x, y)
                    x_times_y = R.mul(x, y)
                else:
                    x_plus_y = x + y
                    x_times_y = x * y
                
                fx = apply_f(f, x)
                fy = apply_f(f, y)
                f_x_plus_y = apply_f(f, x_plus_y)
                f_x_times_y = apply_f(f, x_times_y)
                
                if hasattr(B, 'add') and hasattr(B, 'mul'):
                    B_fx_plus_fy = B.add(fx, fy)
                    B_fx_times_fy = B.mul(fx, fy)
                else:
                    B_fx_plus_fy = fx + fy
                    B_fx_times_fy = fx * fy
                
                if f_x_plus_y != B_fx_plus_fy:
                    h2 = False
                if f_x_times_y != B_fx_times_fy:
                    h2 = False
                    
        if hasattr(R, 'one') and hasattr(B, 'one'):
            if apply_f(f, R.one) != B.one:
                h2 = False
        elif R in (ZZ, QQ) and B in (ZZ, QQ):
            if apply_f(f, 1) != 1:
                h2 = False
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        test_R = get_test_elements(R)
        B_zero = B.zero if hasattr(B, 'zero') else 0
        
        for x in test_R:
            if hasattr(R, 'mul') and hasattr(R, 'add') and hasattr(R, 'neg'):
                x2 = R.mul(x, x)
                minus_x = R.neg(x)
                val = R.add(x2, minus_x)
            else:
                val = x**2 - x
            
            if apply_f(f, val) != B_zero:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict) and 'R_add' in witness:
        return check_dict_format(witness)
    else:
        return check_tuple_format(witness)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a ring homomorphism from R to B",
    "¬Q: The kernel of f does not contain the ideal generated by {x^2 - x | x in R}"
]

N_HYP = 2
NEG_Q_INDEX = 2