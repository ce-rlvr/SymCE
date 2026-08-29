import sympy

# No specific top-level bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
    
    # H_1: a^2 + b^2 = c^2
    try:
        diff = sympy.sympify(a)**2 + sympy.sympify(b)**2 - sympy.sympify(c)**2
        h1 = bool(sympy.simplify(diff) == 0)
    except Exception:
        h1 = False
        
    # neg_Q: abc is NOT divisible by 60
    # Divisibility by 60 in this context means the product is an integer multiple of 60.
    try:
        prod = sympy.sympify(a) * sympy.sympify(b) * sympy.sympify(c)
        val = sympy.simplify(prod / 60)
        if val.is_integer:
            is_div_60 = True
        else:
            try:
                is_div_60 = bool(val == sympy.floor(val))
            except Exception:
                is_div_60 = False
        neg_q = not is_div_60
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "¬Q: abc is not divisible by 60"
]

N_HYP = 1
NEG_Q_INDEX = 1