import sympy
from sympy.abc import x, y, z
import itertools

# Top-level setup
# No specific named objects are strictly required for this domain.
# The witness should provide the rings R and S, the homomorphism f, and elements x, y.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', [])
            S = witness.get('S', [])
            f = witness.get('f', {})
            x_val = witness.get('x', None)
            y_val = witness.get('y', None)
        else:
            R = getattr(witness, 'R', [])
            S = getattr(witness, 'S', [])
            f = getattr(witness, 'f', {})
            x_val = getattr(witness, 'x', None)
            y_val = getattr(witness, 'y', None)
    except Exception:
        return [False, False, False, False, False]

    def get_op(name, default_int, default_set, default_obj):
        if isinstance(witness, dict):
            op = witness.get(name)
        else:
            op = getattr(witness, name, None)
        if op: return op
        def default_op(a, b):
            if isinstance(a, bool) and isinstance(b, bool): return default_int(int(a), int(b))
            if isinstance(a, int) and isinstance(b, int): return default_int(a, b)
            if isinstance(a, (set, frozenset)) and isinstance(b, (set, frozenset)): return default_set(a, b)
            return default_obj(a, b)
        return default_op

    R_add = get_op('R_add', lambda a, b: a ^ b, lambda a, b: a ^ b, lambda a, b: a + b)
    R_mul = get_op('R_mul', lambda a, b: a & b, lambda a, b: a & b, lambda a, b: a * b)
    S_add = get_op('S_add', lambda a, b: a ^ b, lambda a, b: a ^ b, lambda a, b: a + b)
    S_mul = get_op('S_mul', lambda a, b: a & b, lambda a, b: a & b, lambda a, b: a * b)

    def contains(lst, val):
        for item in lst:
            if item == val:
                return True
        return False

    def is_boolean_ring(ring, add_op, mul_op):
        if not isinstance(ring, (list, set, tuple)) or len(ring) == 0:
            return False
        r_list = list(ring)
        
        z_elem = None
        for cand in r_list:
            is_z = True
            for a in r_list:
                if add_op(a, cand) != a or add_op(cand, a) != a:
                    is_z = False
                    break
            if is_z:
                z_elem = cand
                break
        if z_elem is None: return False

        for a in r_list:
            if not contains(r_list, mul_op(a, a)): return False
            if mul_op(a, a) != a: return False
            if add_op(a, a) != z_elem: return False
            for b in r_list:
                ab_add = add_op(a, b)
                ab_mul = mul_op(a, b)
                if not contains(r_list, ab_add): return False
                if not contains(r_list, ab_mul): return False
                if add_op(a, b) != add_op(b, a): return False
                if mul_op(a, b) != mul_op(b, a): return False
                for c in r_list:
                    if add_op(add_op(a, b), c) != add_op(a, add_op(b, c)): return False
                    if mul_op(mul_op(a, b), c) != mul_op(a, mul_op(b, c)): return False
                    if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)): return False
        return True

    # H1: R is a Boolean ring
    try:
        h1 = is_boolean_ring(R, R_add, R_mul)
    except Exception:
        h1 = False

    # H2: S is a Boolean ring
    try:
        h2 = is_boolean_ring(S, S_add, S_mul)
    except Exception:
        h2 = False

    def get_apply_f(f_obj):
        if isinstance(f_obj, dict):
            def apply_f(val):
                for k, v in f_obj.items():
                    if k == val: return v
                raise KeyError(f"Value {val} not found in f")
            return apply_f
        return f_obj

    apply_f = get_apply_f(f)

    # H3: f is a ring homomorphism from R to S
    try:
        h3 = False
        if h1 and h2:
            r_list = list(R)
            s_list = list(S)
            valid = True
            for a in r_list:
                try:
                    fa = apply_f(a)
                    if not contains(s_list, fa):
                        valid = False
                        break
                except Exception:
                    valid = False
                    break
            
            if valid:
                homo = True
                for a in r_list:
                    for b in r_list:
                        fa = apply_f(a)
                        fb = apply_f(b)
                        if apply_f(R_add(a, b)) != S_add(fa, fb):
                            homo = False
                            break
                        if apply_f(R_mul(a, b)) != S_mul(fa, fb):
                            homo = False
                            break
                    if not homo:
                        break
                
                if homo:
                    one_R = None
                    for cand in r_list:
                        if all(R_mul(a, cand) == a for a in r_list):
                            one_R = cand
                            break
                    one_S = None
                    for cand in s_list:
                        if all(S_mul(a, cand) == a for a in s_list):
                            one_S = cand
                            break
                    if one_R is not None and one_S is not None:
                        if apply_f(one_R) != one_S:
                            homo = False
                h3 = homo
    except Exception:
        h3 = False

    # H4: x and y are in R
    try:
        h4 = False
        if h1:
            if contains(list(R), x_val) and contains(list(R), y_val):
                h4 = True
    except Exception:
        h4 = False

    # neg_Q: f(x) <= f(y) is FALSE
    try:
        neg_q = False
        if h3 and h4:
            fx = apply_f(x_val)
            fy = apply_f(y_val)
            if S_mul(fx, fy) != fx:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a Boolean ring",
    "H_3: f is a ring homomorphism from R to S",
    "H_4: x and y are elements of R",
    "¬Q: f(x) <= f(y) is false in S"
]

N_HYP = 4
NEG_Q_INDEX = 4