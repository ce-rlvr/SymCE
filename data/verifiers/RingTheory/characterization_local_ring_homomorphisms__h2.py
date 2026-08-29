import sympy
from sympy import Rational, Integer

def make_Zn(n):
    return {
        'elements': list(range(n)),
        'add': lambda a, b: (a + b) % n,
        'mul': lambda a, b: (a * b) % n,
        'zero': 0,
        'one': 1 % n
    }

# Provide some standard local rings for convenience in witness construction
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z8 = make_Zn(8)
Z9 = make_Zn(9)

def sets_equal(A, B):
    for a in A:
        if a not in B: return False
    for b in B:
        if b not in A: return False
    return True

def is_comm_ring_with_1(elements, add, mul, zero, one):
    if zero not in elements or one not in elements: return False
    n_el = len(elements)
    if n_el > 100 or n_el < 1: return False
    
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
        if mul(a, one) != a: return False
        if mul(one, a) != a: return False
        
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            try:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
            except Exception:
                return False
            if ab_add not in elements: return False
            if ab_mul not in elements: return False
            if ab_add != add(b, a): return False
            if ab_mul != mul(b, a): return False
            
            for c in elements:
                if add(ab_add, c) != add(a, add(b, c)): return False
                if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    return True

def is_ideal(elements, add, mul, zero, I):
    if zero not in I: return False
    for x in I:
        if x not in elements: return False
        has_inv = False
        for y in I:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for y in I:
            if add(x, y) not in I: return False
        for r in elements:
            if mul(r, x) not in I: return False
    return True

def is_local_ring_with_maximal_ideal(elements, add, mul, zero, one, m):
    if not is_comm_ring_with_1(elements, add, mul, zero, one):
        return False
    
    non_units = []
    for x in elements:
        is_unit = False
        for y in elements:
            if mul(x, y) == one:
                is_unit = True
                break
        if not is_unit:
            non_units.append(x)
            
    if not sets_equal(m, non_units):
        return False
        
    return is_ideal(elements, add, mul, zero, non_units)

def conditions(witness):
    try:
        f = witness['f']
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
    except Exception:
        return [False, False]
        
    try:
        R = witness['R']
        R_add = witness['R_add']
        R_mul = witness['R_mul']
        R_zero = witness['R_zero']
        R_one = witness['R_one']
        m = witness['m']
        
        S = witness['S']
        S_add = witness['S_add']
        S_mul = witness['S_mul']
        S_zero = witness['S_zero']
        S_one = witness['S_one']
        n = witness['n']
        
        R_ok = is_local_ring_with_maximal_ideal(R, R_add, R_mul, R_zero, R_one, m)
        S_ok = is_local_ring_with_maximal_ideal(S, S_add, S_mul, S_zero, S_one, n)
        
        f_ok = True
        for x in R:
            if f_func(x) not in S:
                f_ok = False
                break
                
        h1 = bool(R_ok and S_ok and f_ok)
    except Exception:
        h1 = False
        
    try:
        A = True
        for x in m:
            if f_func(x) not in n:
                A = False
                break
                
        f_inv_n = []
        for x in R:
            if f_func(x) in n:
                f_inv_n.append(x)
                
        B = sets_equal(f_inv_n, m)
        
        Q = (A == B)
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: R and S are local rings with unique maximal ideals m and n respectively",
    "¬Q: The equivalence f(m) <= n iff f^-1(n) == m fails"
]

N_HYP = 1
NEG_Q_INDEX = 1