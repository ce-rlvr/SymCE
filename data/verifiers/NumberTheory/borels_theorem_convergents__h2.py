import sympy

# Top-level setup
# No specific named objects needed for this domain

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        x, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: x is an irrational number
    try:
        if x.is_irrational is True:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: n >= 1 is an integer
    try:
        n_sym = sympy.sympify(n)
        h2 = bool(n_sym.is_integer and n_sym >= 1)
    except Exception:
        h2 = False
        
    # ¬Q: For all i in {n-1, n, n+1}, |x - p_i/q_i| >= 1 / (sqrt(5) q_i^2)
    try:
        n_int = int(n_sym)
        max_i = n_int + 1
        
        prec = 2000
        x_val = x.evalf(prec)
        
        p_minus2, p_minus1 = 0, 1
        q_minus2, q_minus1 = 1, 0
        
        convergents = []
        val = x_val
        for i in range(max_i + 1):
            a_i = int(sympy.floor(val))
            p_i = a_i * p_minus1 + p_minus2
            q_i = a_i * q_minus1 + q_minus2
            convergents.append((p_i, q_i))
            
            p_minus2, p_minus1 = p_minus1, p_i
            q_minus2, q_minus1 = q_minus1, q_i
            
            rem = val - a_i
            if rem < 10**(-prec/2):
                break
            val = 1 / rem
            
        neg_q = True
        for i in [n_int - 1, n_int, n_int + 1]:
            if i < 0 or i >= len(convergents):
                neg_q = False
                break
            
            p_i, q_i = convergents[i]
            
            diff = abs(x - sympy.Rational(p_i, q_i))
            threshold = 1 / (sympy.sqrt(5) * q_i**2)
            
            # If diff < threshold, the conclusion holds, so negated conclusion fails
            if (diff - threshold).evalf(prec) < 0:
                neg_q = False
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "H_2: n >= 1 is an integer",
    "¬Q: For all i in {n-1, n, n+1}, |x - p_i/q_i| >= 1 / (sqrt(5) q_i^2)"
]

N_HYP = 2
NEG_Q_INDEX = 2