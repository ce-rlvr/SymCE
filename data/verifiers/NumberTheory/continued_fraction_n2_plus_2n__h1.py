import sympy as sp

def conditions(witness):
    try:
        n = sp.sympify(witness)
    except Exception:
        return [False, False]
        
    # H_1: n >= 1
    try:
        h1_ok = bool(n.is_real and n >= 1)
    except Exception:
        h1_ok = False
        
    # Conclusion: The simple continued fraction expansion of sqrt(n^2 + 2n) is purely periodic 
    # after the first term and is given by [n; 1, 2n, 1, 2n, ...]
    try:
        val = sp.sqrt(n**2 + 2*n)
        v = sp.N(val, 200)
        terms = []
        for _ in range(5):
            f = sp.floor(v)
            terms.append(f)
            if sp.Abs(v - f) < 1e-100:
                break
            v = 1 / (v - f)
        
        expected = [n, 1, 2*n, 1, 2*n]
        
        q_holds = True
        if len(terms) < 5:
            q_holds = False
        else:
            for t, e in zip(terms, expected):
                if float(sp.Abs(t - e)) > 1e-9:
                    q_holds = False
                    break
                    
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "¬Q: The simple continued fraction expansion of sqrt(n^2 + 2n) is not (n; 1, 2n, 1, 2n, ...)"
]

N_HYP = 1
NEG_Q_INDEX = 1