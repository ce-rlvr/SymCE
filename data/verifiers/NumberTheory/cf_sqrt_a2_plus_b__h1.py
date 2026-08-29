import math

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        a, b = witness
        if int(a) != a or int(b) != b:
            return [False, False]
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False]
        
    # H1: b divides 2a
    try:
        h1 = (b != 0) and ((2 * a) % b == 0)
    except Exception:
        h1 = False
        
    # Conclusion: CF is [a; \overline{2a/b, 2a}]
    try:
        if b == 0:
            q = False
        elif (2 * a) % b != 0:
            q = False
        else:
            term1 = (2 * a) // b
            term2 = 2 * a
            
            formula_seq = [a]
            for i in range(20):
                formula_seq.append(term1 if i % 2 == 0 else term2)
                
            n = a**2 + b
            if n < 0:
                q = False
            else:
                r = math.isqrt(n)
                if r * r == n:
                    q = False
                else:
                    m = 0
                    d = 1
                    a_curr = r
                    actual_seq = [a_curr]
                    
                    for _ in range(20):
                        m = d * a_curr - m
                        d = (n - m * m) // d
                        a_curr = (r + m) // d
                        actual_seq.append(a_curr)
                        
                    q = (formula_seq == actual_seq)
    except Exception:
        q = False
        
    neg_q = not q
    
    return [h1, neg_q]

CONDITION_LABELS = ['H_1: b divides 2a', 'neg_Q: CF is not a, 2a/b, 2a']
N_HYP = 1
NEG_Q_INDEX = 1