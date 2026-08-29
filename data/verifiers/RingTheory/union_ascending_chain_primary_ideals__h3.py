import itertools

def get_val(w, key):
    if isinstance(w, dict):
        return w[key]
    return getattr(w, key)

# Top-level setup
R_elements = [(a, b, c) for a in (0,1) for b in (0,1) for c in (0,1)]
zero = (0, 0, 0)
one = (1, 0, 0)

def ring_add(u, v):
    return ((u[0]+v[0])%2, (u[1]+v[1])%2, (u[2]+v[2])%2)

def ring_mul(u, v):
    return ((u[0]*v[0])%2, (u[0]*v[1] + u[1]*v[0])%2, (u[0]*v[2] + u[2]*v[0])%2)

P_ideal = [(0, b, c) for b in (0,1) for c in (0,1)]
Q1_ideal = [(0, 0, 0), (0, 1, 0)]
Q2_ideal = [(0, 0, 0), (0, 0, 1)]

standard_witness = {
    "R": R_elements,
    "add": ring_add,
    "mul": ring_mul,
    "zero": zero,
    "one": one,
    "P": P_ideal,
    "Q_list": [Q1_ideal, Q2_ideal]
}

def is_ideal(R, add, mul, zero, I):
    I_set = set(I)
    if not I_set.issubset(set(R)): return False
    if zero not in I_set: return False
    for a in I_set:
        for b in I_set:
            if add(a, b) not in I_set:
                return False
    for a in I_set:
        for r in R:
            if mul(a, r) not in I_set:
                return False
            if mul(r, a) not in I_set:
                return False
    return True

def is_prime_ideal(R, add, mul, zero, one, P):
    if not is_ideal(R, add, mul, zero, P): return False
    if one in P: return False
    P_set = set(P)
    for a in R:
        for b in R:
            if mul(a, b) in P_set:
                if a not in P_set and b not in P_set:
                    return False
    return True

def radical(R, mul, I):
    I_set = set(I)
    rad = set()
    for val in R:
        curr = val
        for _ in range(len(R)):
            if curr in I_set:
                rad.add(val)
                break
            curr = mul(curr, val)
    return rad

def is_primary_ideal(R, add, mul, zero, one, Q, P):
    if not is_ideal(R, add, mul, zero, Q): return False
    if one in Q: return False
    Q_set = set(Q)
    P_set = set(P)
    
    if radical(R, mul, Q) != P_set:
        return False
        
    for a in R:
        for b in R:
            if mul(a, b) in Q_set:
                if a not in Q_set and b not in P_set:
                    return False
    return True

def check_commutative_ring(witness):
    try:
        R = get_val(witness, "R")
        add = get_val(witness, "add")
        mul = get_val(witness, "mul")
        zero = get_val(witness, "zero")
        one = get_val(witness, "one")
        
        R_set = set(R)
        if zero not in R_set or one not in R_set: return False
        for a in R:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            
            has_inv = False
            for b in R:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in R:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if ab_add not in R_set: return False
                if ab_mul not in R_set: return False
                if ab_add != add(b, a): return False
                if ab_mul != mul(b, a): return False
                for c in R:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
        return True
    except Exception:
        return False

def check_prime_ideal(witness):
    try:
        R = get_val(witness, "R")
        add = get_val(witness, "add")
        mul = get_val(witness, "mul")
        zero = get_val(witness, "zero")
        one = get_val(witness, "one")
        P = get_val(witness, "P")
        return is_prime_ideal(R, add, mul, zero, one, P)
    except Exception:
        return False

def check_Q_primary(witness):
    try:
        R = get_val(witness, "R")
        add = get_val(witness, "add")
        mul = get_val(witness, "mul")
        zero = get_val(witness, "zero")
        one = get_val(witness, "one")
        P = get_val(witness, "P")
        Q_list = get_val(witness, "Q_list")
        if not Q_list: return False
        
        for Q in Q_list:
            if not is_primary_ideal(R, add, mul, zero, one, Q, P):
                return False
        return True
    except Exception:
        return False

def check_union_not_primary(witness):
    try:
        R = get_val(witness, "R")
        add = get_val(witness, "add")
        mul = get_val(witness, "mul")
        zero = get_val(witness, "zero")
        one = get_val(witness, "one")
        P = get_val(witness, "P")
        Q_list = get_val(witness, "Q_list")
        
        union = set()
        for Q in Q_list:
            union.update(Q)
            
        return not is_primary_ideal(R, add, mul, zero, one, list(union), P)
    except Exception:
        return False

def conditions(witness):
    return [
        check_commutative_ring(witness),
        check_prime_ideal(witness),
        check_Q_primary(witness),
        check_union_not_primary(witness)
    ]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal in R",
    "H_3: For all i >= 1, Q_i is a P-primary ideal",
    "¬Q: The union of Q_i is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3