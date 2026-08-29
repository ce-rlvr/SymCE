import math
import sympy

def conditions(witness):
    try:
        a = sympy.sympify(witness)
        if not a.is_number:
            return [False]
        if not a.is_Integer:
            return [True]
        a = int(a)
        
        d = a**2 + 2
        a0 = math.isqrt(d)
        actual_terms = [a0]
        m = 0
        denom = 1
        
        for _ in range(15):
            m = denom * actual_terms[-1] - m
            if denom == 0:
                break
            denom = (d - m**2) // denom
            if denom == 0:
                break
            next_a = (math.isqrt(d) + m) // denom
            actual_terms.append(next_a)
            
        formula_terms = [a]
        for i in range(15):
            if i % 2 == 0:
                formula_terms.append(a)
            else:
                formula_terms.append(2 * a)
                
        neg_q = actual_terms != formula_terms
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["neg_Q: The simple continued fraction expansion of sqrt(a**2+2) is not a; a, 2a"]

N_HYP = 0
NEG_Q_INDEX = 0