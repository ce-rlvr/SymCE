import math
from sympy.ntheory import factorint

# Expected witness format: a tuple of 4 integers (q, k, l, a)
# where q, k, l are the sizes of the finite fields F_q, K, L respectively.
# a is the discrete logarithm of alpha in L^*, with a = -1 representing alpha = 0.

def is_prime_power(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def is_extension(E_size, F_size):
    if not isinstance(E_size, int) or not isinstance(F_size, int):
        return False
    if F_size < 2 or E_size < 2:
        return False
    f_factors = factorint(F_size)
    e_factors = factorint(E_size)
    if len(f_factors) != 1 or len(e_factors) != 1:
        return False
    p1 = list(f_factors.keys())[0]
    p2 = list(e_factors.keys())[0]
    if p1 != p2:
        return False
    exp1 = f_factors[p1]
    exp2 = e_factors[p2]
    return exp2 % exp1 == 0 and exp2 >= exp1

def conditions(witness):
    try:
        q, k, l, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F_q is a finite field with q elements
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H2: L is a finite field extension of K
    try:
        h2 = is_prime_power(k) and is_prime_power(l) and is_extension(l, k)
    except Exception:
        h2 = False
        
    # H3: alpha is an element of L
    try:
        h3 = isinstance(a, int) and not isinstance(a, bool) and -1 <= a < l - 1
    except Exception:
        h3 = False
        
    # neg_Q: N_{L/F_q}(alpha) == N_{K/F_q}(N_{L/K}(alpha)) should FAIL
    try:
        def norm(E_size, F_size, alpha_exp):
            if not is_extension(E_size, F_size):
                raise ValueError("Not an extension")
            if alpha_exp == -1:
                return -1
            return alpha_exp % (F_size - 1)
            
        lhs = norm(l, q, a)
        inner = norm(l, k, a)
        rhs = norm(k, q, inner)
        q_holds = (lhs == rhs)
    except Exception:
        # If any norm is undefined (e.g., K is not an extension of F_q), the equality is meaningless/False
        q_holds = False
        
    neg_q = not q_holds
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: L is a finite field extension of K",
    "H_3: alpha is an element of L",
    "¬Q: N_{L/F_q}(alpha) != N_{K/F_q}(N_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3