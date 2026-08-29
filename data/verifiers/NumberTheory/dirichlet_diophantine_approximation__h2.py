import sympy as sp

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        alpha, N = witness
    except Exception:
        return [False, False]
    
    # H1: alpha is a real number
    try:
        alpha_sp = sp.sympify(alpha)
        if alpha_sp.is_real is not None:
            h1 = bool(alpha_sp.is_real)
        else:
            h1 = bool(sp.im(alpha_sp) == 0)
    except Exception:
        h1 = False

    # neg_Q: Conclusion fails
    try:
        N_sp = sp.sympify(N)
        conclusion_holds = False
        
        if N_sp.is_real != False:
            try:
                if N_sp >= 1:
                    max_q = int(sp.floor(N_sp))
                    threshold = 1 / (N_sp + 1)
                    for q in range(1, max_q + 1):
                        val = q * alpha_sp
                        p_floor = sp.floor(val)
                        p_ceil = sp.ceiling(val)
                        
                        diff1 = abs(val - p_floor)
                        diff2 = abs(val - p_ceil)
                        
                        rel1 = diff1 <= threshold
                        rel2 = diff2 <= threshold
                        
                        if rel1 == True or rel2 == True:
                            conclusion_holds = True
                            break
                        
                        try:
                            if float(diff1) <= float(threshold) or float(diff2) <= float(threshold):
                                conclusion_holds = True
                                break
                        except Exception:
                            pass
            except TypeError:
                # If N_sp >= 1 cannot be evaluated (e.g., symbolic), assume conclusion fails
                pass
        neg_q = not conclusion_holds
    except Exception:
        # If any exception occurs during evaluation, the conclusion statement is invalid/fails.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is a real number",
    "¬Q: There do not exist integers p and q such that 1 <= q <= N and |q*alpha - p| <= 1/(N+1)"
]

N_HYP = 1
NEG_Q_INDEX = 1