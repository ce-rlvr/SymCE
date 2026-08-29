import sympy

n = sympy.Symbol('n', integer=True, positive=True)
k = sympy.Symbol('k', integer=True, positive=True)
i = sympy.Symbol('i', integer=True, positive=True)
m = sympy.Symbol('m', integer=True, positive=True)
j = sympy.Symbol('j', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            expr = witness(n)
            sum_var = n
        else:
            expr = sympy.sympify(witness)
            free_vars = getattr(expr, 'free_symbols', set())
            if n in free_vars:
                sum_var = n
            elif k in free_vars:
                sum_var = k
            elif i in free_vars:
                sum_var = i
            elif m in free_vars:
                sum_var = m
            elif j in free_vars:
                sum_var = j
            else:
                sum_var = n
                
        s = sympy.Sum(expr, (sum_var, 1, sympy.oo)).doit()
        
        if s == sympy.pi**2 / 6:
            is_pi2_6 = True
        else:
            eq = s.equals(sympy.pi**2 / 6)
            is_pi2_6 = (eq is True)
            
        neg_q = not is_pi2_6
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The infinite series does not converge exactly to pi^2/6"
]

N_HYP = 0
NEG_Q_INDEX = 0