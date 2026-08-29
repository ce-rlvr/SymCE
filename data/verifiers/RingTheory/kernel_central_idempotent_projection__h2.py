import sympy
from sympy import Matrix, zeros, eye

# Top-level setup for potential witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def add(a, b, mod=None):
    if hasattr(a, 'applyfunc'):
        c = a + b
        if mod is not None:
            c = c.applyfunc(lambda x: x % mod)
        return c
    else:
        c = a + b
        if mod is not None:
            c = c % mod
        return c

def mul(a, b, mod=None):
    if hasattr(a, 'applyfunc'):
        c = a * b
        if mod is not None:
            c = c.applyfunc(lambda x: x % mod)
        return c
    else:
        c = a * b
        if mod is not None:
            c = c % mod
        return c

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def get_zero(R, mod=None):
    for z in R:
        is_z = True
        for a in R:
            if add(a, z, mod) != a or add(z, a, mod) != a:
                is_z = False
                break
        if is_z:
            return z
    return None

def get_one(R, mod=None):
    for u in R:
        is_u = True
        for a in R:
            if mul(a, u, mod) != a or mul(u, a, mod) != a:
                is_u = False
                break
        if is_u:
            return u
    return None

def neg(a, R, mod=None):
    zero = get_zero(R, mod)
    for x in R:
        if add(a, x, mod) == zero and add(x, a, mod) == zero:
            return x
    return None

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            R, e = witness
            mod = None
        elif len(witness) == 3:
            R, e, mod = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a ring and e is in R
    try:
        h1_ok = False
        if R and contains(R, e):
            zero = get_zero(R, mod)
            one = get_one(R, mod)
            if zero is not None and one is not None:
                is_ring = True
                for a in R:
                    if neg(a, R, mod) is None:
                        is_ring = False
                        break
                    for b in R:
                        if not contains(R, add(a, b, mod)):
                            is_ring = False
                            break
                        if not contains(R, mul(a, b, mod)):
                            is_ring = False
                            break
                        if add(a, b, mod) != add(b, a, mod):
                            is_ring = False
                            break
                        for c in R:
                            if add(add(a, b, mod), c, mod) != add(a, add(b, c, mod), mod):
                                is_ring = False
                                break
                            if mul(mul(a, b, mod), c, mod) != mul(a, mul(b, c, mod), mod):
                                is_ring = False
                                break
                            if mul(a, add(b, c, mod), mod) != add(mul(a, b, mod), mul(a, c, mod), mod):
                                is_ring = False
                                break
                            if mul(add(a, b, mod), c, mod) != add(mul(a, c, mod), mul(b, c, mod), mod):
                                is_ring = False
                                break
                        if not is_ring: break
                    if not is_ring: break
                h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H_2: f(x) = ex maps R into eRe
    try:
        h2_ok = False
        if R and contains(R, e):
            eRe = []
            for r in R:
                ere = mul(e, mul(r, e, mod), mod)
                if not contains(eRe, ere):
                    eRe.append(ere)
            
            maps_into = True
            for x in R:
                fx = mul(e, x, mod)
                if not contains(eRe, fx):
                    maps_into = False
                    break
            h2_ok = maps_into
    except Exception:
        h2_ok = False

    # neg_Q: f is not a surjective ring homomorphism or ker(f) != (1-e)R
    try:
        neg_q_ok = False
        eRe = []
        for r in R:
            ere = mul(e, mul(r, e, mod), mod)
            if not contains(eRe, ere):
                eRe.append(ere)
                
        zero_R = get_zero(R, mod)
        one_R = get_one(R, mod)
        zero_eRe = get_zero(eRe, mod)
        one_eRe = get_one(eRe, mod)
        
        q_holds = True
        
        if one_R is None or zero_R is None or one_eRe is None or zero_eRe is None:
            q_holds = False
        else:
            # 1. f is a ring homomorphism (must map 1_R to 1_eRe)
            if mul(e, one_R, mod) != one_eRe:
                q_holds = False
            
            if q_holds:
                for x in R:
                    for y in R:
                        f_x_plus_y = mul(e, add(x, y, mod), mod)
                        fx_plus_fy = add(mul(e, x, mod), mul(e, y, mod), mod)
                        if f_x_plus_y != fx_plus_fy:
                            q_holds = False
                            break
                            
                        f_xy = mul(e, mul(x, y, mod), mod)
                        fx_fy = mul(mul(e, x, mod), mul(e, y, mod), mod)
                        if f_xy != fx_fy:
                            q_holds = False
                            break
                    if not q_holds: break
            
            # 2. f is surjective
            if q_holds:
                for y in eRe:
                    is_hit = False
                    for x in R:
                        if mul(e, x, mod) == y:
                            is_hit = True
                            break
                    if not is_hit:
                        q_holds = False
                        break
                        
            # 3. ker(f) == (1-e)R
            if q_holds:
                neg_e = neg(e, R, mod)
                if neg_e is None:
                    q_holds = False
                else:
                    one_minus_e = add(one_R, neg_e, mod)
                    
                    ideal = []
                    for x in R:
                        v = mul(one_minus_e, x, mod)
                        if not contains(ideal, v):
                            ideal.append(v)
                            
                    ker = []
                    for x in R:
                        if mul(e, x, mod) == zero_eRe:
                            if not contains(ker, x):
                                ker.append(x)
                                
                    if len(ker) != len(ideal):
                        q_holds = False
                    else:
                        for x in ker:
                            if not contains(ideal, x):
                                q_holds = False
                                break
                                
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring and e is in R",
    "H_2: f(x) = ex maps R into eRe",
    "¬Q: f is not a surjective ring homomorphism or ker(f) != (1-e)R"
]

N_HYP = 2
NEG_Q_INDEX = 2