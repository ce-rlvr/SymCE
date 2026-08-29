import math
from sympy import isprime, primefactors

# Top-level setup
# Witnesses are expected to be tuples of integers representing ideals and elements in ZZ.
# Example witness: (6, [2, 3], [2, 3], 6)
# which corresponds to I=(6), q_1=(2), q_2=(3), P_1=(2), P_2=(3), x=6.

def get_lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def lcm_list(lst):
    if not lst:
        return 1
    res = abs(int(lst[0]))
    for a in lst[1:]:
        res = get_lcm(res, abs(int(a)))
    return res

def is_primary(q):
    try:
        q = int(q)
        if q == 0:
            return True
        if q == 1 or q == -1:
            return False
        q = abs(q)
        factors = primefactors(q)
        return len(factors) == 1
    except Exception:
        return False

def radical(q):
    try:
        q = int(q)
        if q == 0:
            return 0
        q = abs(q)
        factors = primefactors(q)
        res = 1
        for p in factors:
            res *= p
        return res
    except Exception:
        return 0

def is_irredundant(I_val, q_list):
    try:
        I_val = int(I_val)
        if abs(I_val) != lcm_list(q_list):
            return False
        for i in range(len(q_list)):
            sub_list = q_list[:i] + q_list[i+1:]
            if abs(I_val) == lcm_list(sub_list):
                return False
        rads = [radical(q) for q in q_list]
        if len(set(rads)) != len(rads):
            return False
        return True
    except Exception:
        return False

def in_ideal(a, I):
    a = int(a)
    I = int(I)
    if I == 0:
        return a == 0
    return a % I == 0

def is_zd_ring(x, I):
    x = int(x)
    I = int(I)
    if in_ideal(x, I):
        return False
    if I == 0:
        return False
    g = math.gcd(x, I)
    return g > 1

def in_union_P(x, P_list):
    for P in P_list:
        if in_ideal(x, P):
            return True
    return False

def conditions(witness):
    try:
        if len(witness) == 5:
            _, I_val, q_list, P_list, x = witness
        elif len(witness) == 4:
            I_val, q_list, P_list, x = witness
        else:
            return [False] * 5
            
        # H1: R is a commutative ring with identity
        H1 = True
        
        # H2: R is a Noetherian ring
        H2 = True
        
        # H3: I = q_1 \cap ... \cap q_n is an irredundant primary decomposition of I
        H3 = True
        for q in q_list:
            if not is_primary(q):
                H3 = False
        if not is_irredundant(I_val, q_list):
            H3 = False
            
        # H4: P_i = \sqrt{q_i} for i = 1, ..., n are the associated primes of I
        H4 = True
        if len(q_list) != len(P_list):
            H4 = False
        else:
            for q, P in zip(q_list, P_list):
                if abs(int(P)) != radical(q):
                    H4 = False
                    
        # Conclusion: x is a zero divisor on R/I iff x belongs to the union of P_i
        is_zd = is_zd_ring(x, I_val)
        in_union = in_union_P(x, P_list)
        
        neg_Q = (is_zd != in_union)
        
        return [H1, H2, H3, H4, neg_Q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: I = q_1 \\cap ... \\cap q_n is an irredundant primary decomposition of I",
    "H_4: P_i = \\sqrt{q_i} for i = 1, ..., n are the associated primes of I",
    "¬Q: x is a zero divisor on R/I XOR x belongs to the union of the associated primes"
]

N_HYP = 4
NEG_Q_INDEX = 4