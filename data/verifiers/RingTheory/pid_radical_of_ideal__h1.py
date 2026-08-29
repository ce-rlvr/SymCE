import sympy as sp

x, y, z = sp.symbols('x y z')

def get_rem(expr):
    basis = [x - x*y*z]
    _, r = sp.reduced(expr, basis, x, y, z, domain='QQ')
    return r

def is_zero_in_R(expr):
    return get_rem(expr) == 0

def is_equal_in_R(expr1, expr2):
    return is_zero_in_R(expr1 - expr2)

def is_unit_in_R(expr):
    rem = get_rem(expr)
    return rem.is_number and rem != 0

def are_associate_in_R(p1, p2):
    p1_rem = get_rem(p1)
    p2_rem = get_rem(p2)
    if p2_rem == 0:
        return p1_rem == 0
    ratio = sp.cancel(p1_rem / p2_rem)
    return ratio.is_number and ratio != 0

def is_prime_in_R(p):
    p_rem = get_rem(p)
    if p_rem == 0: return False
    if p_rem.is_number: return False
    
    ratio1 = sp.cancel(p_rem / x)
    if ratio1.is_number and ratio1 != 0: return True
    
    ratio2 = sp.cancel(p_rem / (x*y))
    if ratio2.is_number and ratio2 != 0: return True
    
    return False

def is_multiple_in_R(p1, p2):
    basis = sp.groebner([p2, x - x*y*z], x, y, z, domain='QQ')
    _, r = sp.reduced(p1, basis, x, y, z, domain='QQ')
    return r == 0

def conditions(witness):
    try:
        a, u, p_list, e_list, x_val, n = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = not is_zero_in_R(a) and not is_unit_in_R(a)
    except Exception:
        h1 = False
        
    try:
        u_is_unit = is_unit_in_R(u)
        
        prod = u
        for p, e in zip(p_list, e_list):
            prod = prod * (p ** e)
        is_prod = is_equal_in_R(a, prod)
        
        primes_ok = all(is_prime_in_R(p) for p in p_list)
        
        non_assoc = True
        for i in range(len(p_list)):
            for j in range(i+1, len(p_list)):
                if are_associate_in_R(p_list[i], p_list[j]):
                    non_assoc = False
                    
        h2 = u_is_unit and is_prod and primes_ok and non_assoc
    except Exception:
        h2 = False
        
    try:
        in_rad = is_multiple_in_R(x_val**n, a)
        
        prod_p = 1
        for p in p_list:
            prod_p = prod_p * p
            
        in_ideal = is_multiple_in_R(x_val, prod_p)
        
        neg_q = in_rad and not in_ideal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is a prime factorization with pairwise non-associate primes",
    "¬Q: The radical of (a) is NOT the principal ideal (p_1 ... p_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2