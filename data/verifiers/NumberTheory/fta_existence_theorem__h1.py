import sympy

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        h1 = bool(n > 1)
    except Exception:
        h1 = False

    try:
        n = sympy.sympify(witness)
        try:
            val = int(n)
            is_integer_val = (n == val)
        except Exception:
            is_integer_val = False
        
        # A number can be written as a product of one or more primes 
        # if and only if it is an integer greater than or equal to 2.
        if is_integer_val and val >= 2:
            q = True
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1",
    "¬Q: n cannot be written as a product of primes"
]

N_HYP = 1
NEG_Q_INDEX = 1