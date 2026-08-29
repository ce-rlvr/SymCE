import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    is_list = False
    expr = None
    try:
        if isinstance(witness, (list, tuple)):
            is_list = True
        elif hasattr(witness, 'subs'):
            expr = witness
        else:
            expr = witness(n)
    except Exception:
        pass

    def get_val(i):
        if is_list:
            if i - 1 < len(witness):
                return float(witness[i-1])
            else:
                return float(witness[-1])
        elif expr is not None:
            return float(expr.subs(n, i))
        else:
            return float(witness(i))

    # H_1: Assume a_n > 0 for all n >= 1
    try:
        h1 = True
        for i in range(1, 100):
            val = get_val(i)
            if val <= 0:
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: The continued fraction C converges to a finite real number if and only if the infinite series sum a_n diverges (must FAIL)
    try:
        sum_diverges = False
        if expr is not None:
            s = sympy.summation(expr, (n, 1, sympy.oo))
            if s == sympy.oo or s == -sympy.oo:
                sum_diverges = True
            elif s.is_finite is True:
                sum_diverges = False
            elif s.is_finite is False:
                sum_diverges = True
            else:
                n_val = 10000
                an = get_val(n_val)
                an1 = get_val(n_val + 1)
                if an == 0:
                    sum_diverges = False
                else:
                    raabe = n_val * (1 - an1 / an)
                    sum_diverges = (raabe <= 1.05)
        else:
            n_val = 10000
            an = get_val(n_val)
            an1 = get_val(n_val + 1)
            if an == 0:
                sum_diverges = False
            else:
                raabe = n_val * (1 - an1 / an)
                sum_diverges = (raabe <= 1.05)
            
        p_prev, p_curr = 1.0, 0.0
        q_prev, q_curr = 0.0, 1.0
        
        for i in range(1, 10000):
            a_i = get_val(i)
            p_next = a_i * p_curr + p_prev
            q_next = a_i * q_curr + q_prev
            
            if q_next > 1e100:
                p_next /= 1e100
                q_next /= 1e100
                p_curr /= 1e100
                q_curr /= 1e100
                
            p_prev, p_curr = p_curr, p_next
            q_prev, q_curr = q_curr, q_next
            
        if q_curr == 0:
            c_converges = False
        else:
            c_prev = p_prev / q_prev if q_prev != 0 else 0
            c_curr = p_curr / q_curr
            c_converges = abs(c_curr - c_prev) < 1e-9
            
        neg_q = not (c_converges == sum_diverges)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_n > 0 for all n >= 1",
    "¬Q: The continued fraction C converges to a finite real number if and only if the infinite series sum a_n diverges is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1