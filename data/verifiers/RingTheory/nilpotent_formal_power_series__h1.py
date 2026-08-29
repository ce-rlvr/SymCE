import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_element(e):
    try:
        if hasattr(e, 'shape'):
            for i in range(e.shape[0]):
                for j in range(e.shape[1]):
                    val = e[i, j]
                    if val != 0 and sympy.expand(val) != 0:
                        return False
            return True
        else:
            return e == 0 or sympy.expand(e) == 0
    except Exception:
        return False

def conditions(witness):
    h1_ok = False
    try:
        if isinstance(witness, list) and len(witness) > 0:
            is_mat = hasattr(witness[0], 'shape')
            if is_mat:
                n = witness[0].shape[0]
                if all(hasattr(c, 'shape') and c.shape[0] == n and c.shape[1] == n for c in witness):
                    h1_ok = True
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if h1_ok:
            is_mat = hasattr(witness[0], 'shape')
            if is_mat:
                n = witness[0].shape[0]
                zero_elem = sympy.zeros(n, n)
            else:
                zero_elem = 0

            curr = witness
            is_nilp = False
            for _ in range(1, 50):
                all_zero = True
                for c in curr:
                    if not is_zero_element(c):
                        all_zero = False
                        break
                if all_zero:
                    is_nilp = True
                    break
                
                res = [zero_elem for _ in range(len(curr) + len(witness) - 1)]
                for i, c1 in enumerate(curr):
                    for j, c2 in enumerate(witness):
                        res[i+j] = res[i+j] + c1 * c2
                curr = res
            h2_ok = is_nilp
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            is_mat = hasattr(witness[0], 'shape')
            if is_mat:
                max_pow = max(witness[0].shape[0], 50)
            else:
                max_pow = 50

            for c in witness:
                curr = c
                c_is_nilp = False
                for _ in range(1, max_pow + 1):
                    if is_zero_element(curr):
                        c_is_nilp = True
                        break
                    curr = curr * c
                if not c_is_nilp:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is an element of the formal power series ring R(x)",
    "H_2: f(x) is nilpotent in R(x)",
    "not Q: For some i >= 0, the coefficient a_i is NOT a nilpotent element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2