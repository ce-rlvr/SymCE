import sympy

def conditions(witness) -> list[bool]:
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = False
        if hasattr(a, '__getitem__') and hasattr(a, '__len__'):
            if len(a) > 0:
                if isinstance(a[0], (int, sympy.Integer)) and not isinstance(a[0], bool):
                    h1 = True
                    for i in range(1, len(a)):
                        x = a[i]
                        if not isinstance(x, (int, sympy.Integer)) or isinstance(x, bool) or x < 1:
                            h1 = False
                            break
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and n >= 1
    except Exception:
        h2 = False

    try:
        p_minus2, q_minus2 = 0, 1
        p_minus1, q_minus1 = 1, 0
        
        p_prev2, q_prev2 = p_minus2, q_minus2
        p_prev, q_prev = p_minus1, q_minus1
        
        for i in range(n + 1):
            ai = a[i]
            pi = ai * p_prev + p_prev2
            qi = ai * q_prev + q_prev2
            
            p_prev2 = p_prev
            p_prev = pi
            q_prev2 = q_prev
            q_prev = qi
            
        pn = p_prev
        qn = q_prev
        pn_minus1 = p_prev2
        qn_minus1 = q_prev2
        
        q_ok = (pn * qn_minus1 - pn_minus1 * qn) == (-1)**(n - 1)
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: a is a simple continued fraction", "H_2: n >= 1 is an integer", "not Q: p_n q_{n-1} - p_{n-1} q_n != (-1)^{n-1}"]
N_HYP = 2
NEG_Q_INDEX = 2