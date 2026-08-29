import sympy

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            p, q = witness
        else:
            p, q = witness.p, witness.q
            
        p = int(p)
        q = int(q)
        
        if q == 0:
            return [False]
            
        num, den = p, q
        if num < 0 and den < 0:
            num, den = -num, -den
        elif den < 0:
            num, den = -num, -den
            
        cf1 = []
        n, d = num, den
        while d != 0:
            cf1.append(n // d)
            n, d = d, n % d
            
        if not cf1:
            cf1 = [0]
            
        cf2 = list(cf1)
        if len(cf2) > 0:
            if cf2[-1] > 1:
                cf2[-1] -= 1
                cf2.append(1)
            elif len(cf2) > 1 and cf2[-1] == 1:
                cf2.pop()
                cf2[-1] += 1
            elif len(cf2) == 1 and cf2[0] == 1:
                cf2 = [0, 1]
                
        def is_sym(cf):
            if not cf: 
                return False
            if cf[0] != 0: 
                return False
            seq = cf[1:]
            return seq == seq[::-1]
            
        A = is_sym(cf1) or is_sym(cf2)
        
        B = ((p**2 - 1) % q == 0) or ((p**2 + 1) % q == 0)
        
        neg_Q = (A != B)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: The equivalence p/q has a symmetric continued fraction iff p^2 == +/-1 mod q FAILS"]

N_HYP = 0
NEG_Q_INDEX = 0