import sympy

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        
        upper_bound = int(sympy.floor(n))
        if upper_bound > 100000:
            return [False]
            
        s = sympy.Integer(0)
        for k in range(1, upper_bound + 1):
            s += sympy.totient(k) * sympy.floor(n / k)
            
        rhs = n * (n + 1) / sympy.Integer(2)
        
        neg_q = bool(sympy.simplify(s - rhs) != 0)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{k=1}^n phi(k) floor(n/k) != n(n+1)/2"
]

N_HYP = 0
NEG_Q_INDEX = 0