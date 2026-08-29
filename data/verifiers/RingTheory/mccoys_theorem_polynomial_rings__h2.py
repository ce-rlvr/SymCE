import sympy
from sympy.matrices import eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_in(a, R):
    return any(eq(a, r) for r in R)

def eq(a, b):
    try:
        if hasattr(a, 'equals'):
            return a.equals(b)
        return a == b
    except Exception:
        return a == b

def safe_add(a, b):
    try:
        return a + b
    except Exception:
        return None

def safe_mul(a, b):
    try:
        return a * b
    except Exception:
        return None

def get_zero_and_one(R):
    zero = None
    for z in R:
        is_z = True
        for a in R:
            az = safe_add(a, z)
            if az is None or not is_in(az, R) or not eq(az, a):
                is_z = False
                break
        if is_z:
            zero = z
            break
            
    one = None
    for u in R:
        is_u = True
        for a in R:
            au = safe_mul(a, u)
            if au is None or not is_in(au, R) or not eq(au, a):
                is_u = False
                break
        if is_u:
            one = u
            break
            
    return zero, one

def poly_mul(f, g, zero):
    if not f or not g:
        return [zero]
    res = [zero] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            term = safe_mul(a, b)
            if term is None:
                return [None]
            s = safe_add(res[i+j], term)
            if s is None:
                return [None]
            res[i+j] = s
    return res

def is_zero_poly(f, zero):
    if f == [None]:
        return False
    return all(eq(c, zero) for c in f)

def conditions(witness):
    try:
        if len(witness) == 3:
            R, f, g = witness
        elif len(witness) == 2:
            R, f = witness
            g = None
        else:
            return [False, False, False, False]
        iter(R)
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        zero, one = get_zero_and_one(R)
        if zero is not None and one is not None and not eq(zero, one):
            is_comm_ring = True
            for a in R:
                if not is_comm_ring: break
                has_neg = False
                for b in R:
                    if not is_comm_ring: break
                    ab_add = safe_add(a, b)
                    ba_add = safe_add(b, a)
                    ab_mul = safe_mul(a, b)
                    ba_mul = safe_mul(b, a)
                    
                    if ab_add is None or not is_in(ab_add, R): is_comm_ring = False
                    if ab_mul is None or not is_in(ab_mul, R): is_comm_ring = False
                    if ba_add is None or not eq(ab_add, ba_add): is_comm_ring = False
                    if ba_mul is None or not eq(ab_mul, ba_mul): is_comm_ring = False
                    
                    if ab_add is not None and eq(ab_add, zero):
                        has_neg = True
                        
                    for c in R:
                        if not is_comm_ring: break
                        ab = ab_add
                        bc = safe_add(b, c)
                        ab_c = safe_add(ab, c) if ab is not None else None
                        a_bc = safe_add(a, bc) if bc is not None else None
                        if ab_c is None or a_bc is None or not eq(ab_c, a_bc): is_comm_ring = False
                        
                        abm = ab_mul
                        bcm = safe_mul(b, c)
                        abm_c = safe_mul(abm, c) if abm is not None else None
                        a_bcm = safe_mul(a, bcm) if bcm is not None else None
                        if abm_c is None or a_bcm is None or not eq(abm_c, a_bcm): is_comm_ring = False
                        
                        acm = safe_mul(a, c)
                        ab_ac = safe_add(abm, acm) if abm is not None and acm is not None else None
                        a_bc_add = safe_mul(a, bc) if bc is not None else None
                        if ab_ac is None or a_bc_add is None or not eq(a_bc_add, ab_ac): is_comm_ring = False
                        
                if not has_neg:
                    is_comm_ring = False
            h1 = is_comm_ring
    except Exception:
        h1 = False

    h2 = False
    try:
        if isinstance(f, list) and len(f) > 0 and all(is_in(c, R) for c in f):
            h2 = True
    except Exception:
        h2 = False

    h3 = False
    try:
        if h1 and h2:
            if g is not None:
                if isinstance(g, list) and len(g) > 0 and all(is_in(c, R) for c in g):
                    if not is_zero_poly(g, zero):
                        fg = poly_mul(f, g, zero)
                        gf = poly_mul(g, f, zero)
                        if is_zero_poly(fg, zero) or is_zero_poly(gf, zero):
                            h3 = True
            else:
                found = False
                max_deg = 3 if len(R) > 16 else 4
                for deg in range(max_deg):
                    for coeffs in itertools.product(R, repeat=deg+1):
                        coeffs = list(coeffs)
                        if is_zero_poly(coeffs, zero):
                            continue
                        fg = poly_mul(f, coeffs, zero)
                        gf = poly_mul(coeffs, f, zero)
                        if is_zero_poly(fg, zero) or is_zero_poly(gf, zero):
                            found = True
                            break
                    if found:
                        break
                h3 = found
    except Exception:
        h3 = False

    neg_q = False
    try:
        if h1 and h2:
            has_annihilator = False
            for r in R:
                if eq(r, zero):
                    continue
                if all(eq(safe_mul(r, c), zero) for c in f):
                    has_annihilator = True
                    break
            neg_q = not has_annihilator
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: c(f) denotes the ideal generated by the coefficients of f",
    "H_3: f is a zero divisor in the polynomial ring",
    "not Q: There is no non-zero element r in R such that r c(f) = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3