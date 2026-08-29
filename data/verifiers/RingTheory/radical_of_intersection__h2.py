import math
from sympy import symbols, Rational, Integer, eye, zeros

# Standard algebra objects for Ring Theory / Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_integer_like(x):
    try:
        return int(x) == x
    except Exception:
        return False

def get_int_roots(subset):
    roots = set()
    for val in subset:
        roots.add(val)
        if val == 0:
            continue
        if val == 1:
            roots.add(-1)
            continue
        if val == -1:
            continue
        
        abs_val = abs(val)
        limit = math.isqrt(abs_val)
        for x in range(-limit, limit + 1):
            if x in (0, 1, -1):
                continue
            curr = x * x
            while abs(curr) <= abs_val:
                if curr == val:
                    roots.add(x)
                    break
                curr *= x
    return roots

def get_zn_roots(subset, n):
    subset_mod = {x % n for x in subset}
    roots = set()
    for x in range(n):
        curr = x % n
        for _ in range(1, n + 2):
            if curr in subset_mod:
                roots.add(x)
                break
            curr = (curr * x) % n
    return roots

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Z_n subsets: witness is (n, S, T)
    try:
        if isinstance(witness, tuple) and len(witness) == 3 and is_integer_like(witness[0]):
            n = int(witness[0])
            S, T = witness[1], witness[2]
            if n > 0:
                S_set = set(S)
                T_set = set(T)
                if all(is_integer_like(x) for x in S_set) and all(is_integer_like(x) for x in T_set):
                    S_set = {int(x) for x in S_set}
                    T_set = {int(x) for x in T_set}
                    h1 = True # Z_n is commutative
                    
                    rad_S = get_zn_roots(S_set, n)
                    rad_T = get_zn_roots(T_set, n)
                    rad_S_int_T = get_zn_roots(S_set.intersection(T_set), n)
                    rad_S_int_rad_T = rad_S.intersection(rad_T)
                    
                    neg_q = (rad_S_int_T != rad_S_int_rad_T)
                    return [h1, neg_q]
    except Exception:
        pass

    # 2. Z subsets: witness is (S, T)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            S, T = witness
            S_set = set(S)
            T_set = set(T)
            if all(is_integer_like(x) for x in S_set) and all(is_integer_like(x) for x in T_set):
                S_set = {int(x) for x in S_set}
                T_set = {int(x) for x in T_set}
                h1 = True # Z is commutative
                
                rad_S = get_int_roots(S_set)
                rad_T = get_int_roots(T_set)
                rad_S_int_T = get_int_roots(S_set.intersection(T_set))
                rad_S_int_rad_T = rad_S.intersection(rad_T)
                
                neg_q = (rad_S_int_T != rad_S_int_rad_T)
                return [h1, neg_q]
    except Exception:
        pass

    # 3. Z subsets with explicit R: witness is (R, S, T)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, T = witness
            S_set = set(S)
            T_set = set(T)
            if all(is_integer_like(x) for x in S_set) and all(is_integer_like(x) for x in T_set):
                S_set = {int(x) for x in S_set}
                T_set = {int(x) for x in T_set}
                
                if (isinstance(R, str) and R in ('Z', 'ZZ')) or (hasattr(R, 'is_commutative') and R.is_commutative):
                    h1 = True
                else:
                    h1 = False
                    
                rad_S = get_int_roots(S_set)
                rad_T = get_int_roots(T_set)
                rad_S_int_T = get_int_roots(S_set.intersection(T_set))
                rad_S_int_rad_T = rad_S.intersection(rad_T)
                
                neg_q = (rad_S_int_T != rad_S_int_rad_T)
                return [h1, neg_q]
    except Exception:
        pass

    # 4. Duck-typing for custom objects
    try:
        R = getattr(witness, 'R', None)
        I = getattr(witness, 'I', None)
        J = getattr(witness, 'J', None)
        
        if R is None and isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
            
        if I is not None and J is not None:
            if R is not None and hasattr(R, 'is_commutative'):
                h1 = R.is_commutative() if callable(R.is_commutative) else R.is_commutative
            else:
                h1 = True
                
            if hasattr(I, 'intersect'):
                I_int_J = I.intersect(J)
            elif hasattr(I, 'intersection'):
                I_int_J = I.intersection(J)
            else:
                I_int_J = I & J
                
            if hasattr(I, 'radical'):
                rad_I = I.radical()
                rad_J = J.radical()
                rad_I_int_J = I_int_J.radical()
            elif R is not None and hasattr(R, 'radical'):
                rad_I = R.radical(I)
                rad_J = R.radical(J)
                rad_I_int_J = R.radical(I_int_J)
            else:
                raise ValueError
                
            if hasattr(rad_I, 'intersect'):
                rad_I_int_rad_J = rad_I.intersect(rad_J)
            elif hasattr(rad_I, 'intersection'):
                rad_I_int_rad_J = rad_I.intersection(rad_J)
            else:
                rad_I_int_rad_J = rad_I & rad_J
                
            neg_q = (rad_I_int_J != rad_I_int_rad_J)
            return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The radical of the intersection I \\cap J is not equal to the intersection of the radical of I and the radical of J"
]

N_HYP = 1
NEG_Q_INDEX = 1