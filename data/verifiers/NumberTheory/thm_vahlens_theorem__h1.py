import sympy
from sympy import Rational, Abs, sympify
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    target_alpha = None
    target_n = None
    target_cf = None
    target_convs = None
    
    # Parse the witness which could be provided in multiple formats
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 5:
                target_alpha, p_n, q_n, p_n1, q_n1 = witness
                target_convs = ((p_n, q_n), (p_n1, q_n1))
            elif len(witness) == 3:
                target_alpha, target_cf, target_n = witness
            elif len(witness) == 2:
                target_alpha, target_n = witness
            elif len(witness) == 1:
                target_alpha = witness[0]
            else:
                target_alpha = witness
        else:
            target_alpha = witness
    except Exception:
        pass

    if target_alpha is None:
        return [False, False]
        
    try:
        alpha_val = sympify(target_alpha)
        if alpha_val.is_Float:
            alpha_val = Rational(alpha_val)
    except Exception:
        return [False, False]
        
    h1_ok = False
    neg_q_ok = False
    
    is_rational = False
    try:
        if alpha_val.is_Rational:
            is_rational = True
    except Exception:
        pass
        
    if is_rational:
        try:
            num, den = alpha_val.p, alpha_val.q
            cf_main = []
            while den != 0:
                cf_main.append(num // den)
                num, den = den, num % den
                
            # A rational number has two simple continued fraction representations
            cfs = []
            if cf_main:
                cfs.append(cf_main)
                if cf_main[-1] > 1:
                    cf2 = cf_main[:]
                    cf2[-1] -= 1
                    cf2.append(1)
                    cfs.append(cf2)
                elif len(cf_main) > 1 and cf_main[-1] == 1:
                    cf2 = cf_main[:-1]
                    cf2[-1] += 1
                    cfs.append(cf2)
                elif len(cf_main) == 1:
                    cf2 = [cf_main[0] - 1, 1]
                    cfs.append(cf2)
                    
            for cf in cfs:
                if target_cf is not None:
                    if list(cf) != list(target_cf):
                        continue
                        
                convs = []
                p_prev2, q_prev2 = 0, 1
                p_prev1, q_prev1 = 1, 0
                for a in cf:
                    p = a * p_prev1 + p_prev2
                    q = a * q_prev1 + q_prev2
                    convs.append((p, q))
                    p_prev2, q_prev2 = p_prev1, q_prev1
                    p_prev1, q_prev1 = p, q
                    
                for n in range(len(convs) - 1):
                    if target_n is not None and n != target_n:
                        continue
                        
                    pn, qn = convs[n]
                    pn1, qn1 = convs[n+1]
                    
                    if target_convs is not None:
                        if target_convs != ((pn, qn), (pn1, qn1)):
                            continue
                            
                    h1_ok = True
                    
                    diff1 = Abs(alpha_val - Rational(pn, qn))
                    thresh1 = Rational(1, 2 * qn**2)
                    
                    diff2 = Abs(alpha_val - Rational(pn1, qn1))
                    thresh2 = Rational(1, 2 * qn1**2)
                    
                    # Negated conclusion: BOTH inequalities must fail (i.e., be >=)
                    if diff1 >= thresh1 and diff2 >= thresh2:
                        neg_q_ok = True
                        break
                if neg_q_ok:
                    break
        except Exception:
            pass
    else:
        # Irrational case (Vahlen's theorem holds, so neg_q_ok will remain False)
        try:
            it = continued_fraction_iterator(alpha_val)
            convs = []
            p_prev2, q_prev2 = 0, 1
            p_prev1, q_prev1 = 1, 0
            
            max_n = target_n if target_n is not None else 0
            if target_convs is not None:
                max_n = max(max_n, 100)
                
            for i, a in enumerate(it):
                p = a * p_prev1 + p_prev2
                q = a * q_prev1 + q_prev2
                convs.append((p, q))
                p_prev2, q_prev2 = p_prev1, q_prev1
                p_prev1, q_prev1 = p, q
                
                if i > max_n + 1:
                    break
                    
            for n in range(len(convs) - 1):
                if target_n is not None and n != target_n:
                    continue
                    
                pn, qn = convs[n]
                pn1, qn1 = convs[n+1]
                
                if target_convs is not None:
                    if target_convs != ((pn, qn), (pn1, qn1)):
                        continue
                        
                h1_ok = True
                break
        except Exception:
            pass
            
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p_n/q_n and p_{n+1}/q_{n+1} are consecutive convergents of the simple continued fraction expansion of alpha",
    "¬Q: Both |alpha - p_n/q_n| >= 1/(2q_n^2) and |alpha - p_{n+1}/q_{n+1}| >= 1/(2q_{n+1}^2) hold"
]
N_HYP = 1
NEG_Q_INDEX = 1