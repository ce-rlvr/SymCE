import sympy

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "not_Q: I \\otimes_R (R/J) is not isomorphic to I/IJ"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', witness.get('R', 1)))
            m = int(witness.get('m', witness.get('J', 2 * n)))
            k = int(witness.get('k', witness.get('I', n)))
        else:
            t = tuple(map(int, witness))
            if len(t) >= 3:
                n, m, k = t[0], t[1], t[2]
            elif len(t) == 2:
                n, m = t
                k = n
            elif len(t) == 1:
                n = t[0]
                m = n * 2
                k = n
            else:
                return [False, False, False]
                
        n, m, k = abs(n), abs(m), abs(k)
        
        h1 = True
        
        if n == 0:
            h2 = (m == 0)
        else:
            h2 = (m % n == 0)
            
        neg_q = (n != 1) and (m != 0) and (k != 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]