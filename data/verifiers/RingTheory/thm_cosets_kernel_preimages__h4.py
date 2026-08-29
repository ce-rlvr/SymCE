import sympy
import math

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_obj = witness.get('R', witness.get('n'))
            S_obj = witness.get('S', witness.get('m'))
            f_obj = witness.get('f', witness.get('a'))
            K = witness.get('K')
            s = witness.get('s')
            r = witness.get('r')
        elif isinstance(witness, (list, tuple)):
            R_obj, S_obj, f_obj, K, s, r = witness
        else:
            R_obj = getattr(witness, 'R', getattr(witness, 'n', None))
            S_obj = getattr(witness, 'S', getattr(witness, 'm', None))
            f_obj = getattr(witness, 'f', getattr(witness, 'a', None))
            K = getattr(witness, 'K', None)
            s = getattr(witness, 's', None)
            r = getattr(witness, 'r', None)
    except Exception:
        return [False, False, False, False]

    def get_ring(obj):
        try:
            if hasattr(obj, '__int__') and not isinstance(obj, bool):
                obj = int(obj)
            if isinstance(obj, int) and obj > 0:
                return list(range(obj)), lambda x, y: (x + y) % obj, lambda x, y: (x * y) % obj, 0
        except Exception:
            pass
        if isinstance(obj, (list, tuple, set)):
            n = len(obj)
            try:
                obj_ints = {int(x) for x in obj}
                if obj_ints == set(range(n)):
                    return list(range(n)), lambda x, y: (x + y) % n, lambda x, y: (x * y) % n, 0
            except Exception:
                pass
        return None, None, None, None

    try:
        R_elements, R_add, R_mul, R_zero = get_ring(R_obj)
        S_elements, S_add, S_mul, S_zero = get_ring(S_obj)
        h1 = (R_elements is not None) and (S_elements is not None)
    except Exception:
        h1 = False

    def get_f_func(f_obj, S_obj):
        if callable(f_obj):
            return f_obj
        elif isinstance(f_obj, dict):
            return lambda x: f_obj[x]
        elif isinstance(f_obj, (list, tuple)):
            return lambda x: f_obj[x]
        try:
            if (isinstance(f_obj, int) or hasattr(f_obj, '__int__')) and not isinstance(f_obj, bool):
                f_val = int(f_obj)
                if hasattr(S_obj, '__int__') and not isinstance(S_obj, bool):
                    m = int(S_obj)
                elif isinstance(S_obj, (list, tuple, set)):
                    m = len(S_obj)
                else:
                    m = 1
                return lambda x: (f_val * x) % m
        except Exception:
            pass
        return None

    try:
        f_func = get_f_func(f_obj, S_obj)
        h2 = False
        if h1 and f_func is not None and K is not None:
            h2 = True
            for x in R_elements:
                fx = f_func(x)
                if fx not in S_elements:
                    h2 = False
                    break
            if h2:
                for x in R_elements:
                    for y in R_elements:
                        if f_func(R_add(x, y)) != S_add(f_func(x), f_func(y)):
                            h2 = False
                        if f_func(R_mul(x, y)) != S_mul(f_func(x), f_func(y)):
                            h2 = False
            if h2:
                expected_K = {int(x) for x in R_elements if f_func(x) == S_zero}
                K_clean = {int(k) for k in K}
                if K_clean != expected_K:
                    h2 = False
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2 and s is not None:
            s_clean = int(s)
            image_f = {int(f_func(x)) for x in R_elements}
            if s_clean in image_f:
                h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and r is not None:
            r_clean = int(r)
            s_clean = int(s)
            if r_clean in R_elements:
                preimage = {int(x) for x in R_elements if int(f_func(x)) == s_clean}
                coset = {int(R_add(r_clean, k)) for k in K}
                if preimage != coset:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism with kernel K",
    "H_3: s is an element in the image of f",
    "¬Q: The preimage f^(-1)({s}) is not exactly the coset r + K"
]

N_HYP = 3
NEG_Q_INDEX = 3