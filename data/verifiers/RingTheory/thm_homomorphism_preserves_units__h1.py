import itertools
from sympy.matrices import eye, zeros
from sympy import Rational, Integer

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism",
    "H_2: f(1_R) = 1_S",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S or f(u^{-1}) != f(u)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    def get_add_R(x, y):
        if hasattr(witness, 'add_R'): return witness.add_R(x, y)
        return x + y

    def get_mul_R(x, y):
        if hasattr(witness, 'mul_R'): return witness.mul_R(x, y)
        return x * y

    def get_add_S(x, y):
        if hasattr(witness, 'add_S'): return witness.add_S(x, y)
        return x + y

    def get_mul_S(x, y):
        if hasattr(witness, 'mul_S'): return witness.mul_S(x, y)
        return x * y

    try:
        f = witness.f
        one_R = witness.one_R
        one_S = witness.one_S
        u = witness.u
    except Exception:
        return [False, False, False, False]

    # H1: f is a ring homomorphism
    try:
        if hasattr(witness, 'is_ring_homomorphism'):
            h1 = bool(witness.is_ring_homomorphism())
        else:
            h1 = True
            if hasattr(witness, 'R'):
                R_sample = list(itertools.islice(witness.R, 100))
                for x in R_sample:
                    for y in R_sample:
                        if not (f(get_add_R(x, y)) == get_add_S(f(x), f(y))):
                            h1 = False
                            break
                        if not (f(get_mul_R(x, y)) == get_mul_S(f(x), f(y))):
                            h1 = False
                            break
                    if not h1:
                        break
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: f(1_R) = 1_S
    try:
        h2 = bool(f(one_R) == one_S)
    except Exception:
        h2 = False

    # H3: u is a unit in R
    try:
        h3 = False
        u_inv = None
        if hasattr(witness, 'R'):
            try:
                R_list = list(witness.R)
                for v in R_list:
                    if get_mul_R(u, v) == one_R and get_mul_R(v, u) == one_R:
                        h3 = True
                        u_inv = v
                        break
            except Exception:
                pass
        
        if not h3 and hasattr(witness, 'u_inv'):
            v = witness.u_inv
            if v is not None:
                if get_mul_R(u, v) == one_R and get_mul_R(v, u) == one_R:
                    h3 = True
                    u_inv = v
    except Exception:
        h3 = False

    # NegQ: f(u) is not a unit in S or f(u^{-1}) != f(u)^{-1}
    try:
        if not h3:
            neg_q = False
        else:
            f_u = f(u)
            
            true_one_S = None
            has_true_id = False
            if hasattr(witness, 'true_one_S'):
                true_one_S = witness.true_one_S
                has_true_id = True
            elif hasattr(witness, 'S'):
                try:
                    S_list = list(witness.S)
                    for e in S_list:
                        is_id = True
                        for x in S_list:
                            if get_mul_S(e, x) != x or get_mul_S(x, e) != x:
                                is_id = False
                                break
                        if is_id:
                            true_one_S = e
                            has_true_id = True
                            break
                except Exception:
                    pass
            
            if not has_true_id and hasattr(witness, 'S'):
                try:
                    S_sample = list(itertools.islice(witness.S, 100))
                    is_id = True
                    for x in S_sample:
                        if get_mul_S(one_S, x) != x or get_mul_S(x, one_S) != x:
                            is_id = False
                            break
                    if is_id:
                        true_one_S = one_S
                        has_true_id = True
                except Exception:
                    pass

            if not has_true_id:
                is_unit_S = False
                f_u_inv_S = None
                searched_all_S = True
            else:
                is_unit_S = False
                f_u_inv_S = None
                searched_all_S = False
                if hasattr(witness, 'S'):
                    try:
                        S_list = list(witness.S)
                        searched_all_S = True
                        for v in S_list:
                            if get_mul_S(f_u, v) == true_one_S and get_mul_S(v, f_u) == true_one_S:
                                is_unit_S = True
                                f_u_inv_S = v
                                break
                    except Exception:
                        pass
                
                if not is_unit_S and hasattr(witness, 'f_u_inv_S'):
                    v = witness.f_u_inv_S
                    if v is not None:
                        if get_mul_S(f_u, v) == true_one_S and get_mul_S(v, f_u) == true_one_S:
                            is_unit_S = True
                            f_u_inv_S = v

            if not is_unit_S:
                if searched_all_S:
                    neg_q = True
                else:
                    if hasattr(witness, 'is_unit_S'):
                        neg_q = not witness.is_unit_S
                    else:
                        neg_q = False
            else:
                neg_q = not (f(u_inv) == f_u_inv_S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]