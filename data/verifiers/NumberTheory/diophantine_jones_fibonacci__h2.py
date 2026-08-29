import sympy

def conditions(witness):
    try:
        # Witness should be a tuple or list of two elements: (x, y)
        if len(witness) != 2:
            return [False, False]
        x, y = witness
    except Exception:
        return [False, False]
    
    # H_1: x and y are positive integers
    try:
        h1 = (isinstance(x, (int, sympy.Integer)) and 
              isinstance(y, (int, sympy.Integer)) and 
              x > 0 and y > 0)
    except Exception:
        h1 = False
        
    # ¬Q: There does not exist an integer n >= 1 such that x = F_{n+1} and y = F_n
    try:
        if not h1:
            neg_q = False
        else:
            is_fib_pair = False
            a, b = 1, 1  # F_1, F_2
            # Since F_n is non-decreasing, we only need to check while F_n <= y
            while a <= y:
                if a == y and b == x:
                    is_fib_pair = True
                    break
                a, b = b, a + b
            neg_q = not is_fib_pair
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are positive integers",
    "¬Q: There does not exist an integer n >= 1 such that x = F_{n+1} and y = F_n"
]

N_HYP = 1
NEG_Q_INDEX = 1