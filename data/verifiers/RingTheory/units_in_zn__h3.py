import sympy
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, n) or a dictionary {'a': a, 'n': n}.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) >= 2:
            a = witness[0]
            n = witness[1]
        else:
            return [False, False, False]
            
        if a is None or n is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 1
    except Exception:
        h1 = False
        
    # H_2: Z_n is the ring of integers modulo n
    # This is a definitional hypothesis, always True in the context of the theorem.
    h2 = True
    
    # ¬Q: It is not the case that (a is a unit in Z_n if and only if gcd(a, n) == 1)
    try:
        # Check if a is a unit in Z_n
        # a is a unit in Z_n if it is an integer and gcd(a, n) == 1
        if isinstance(a, (int, sympy.Integer)):
            is_unit = (math.gcd(int(a), int(n)) == 1)
        else:
            is_unit = False
            
        # Check gcd(a, n) == 1
        if isinstance(a, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)):
            gcd_val = math.gcd(int(a), int(n))
        else:
            gcd_val = sympy.gcd(a, n)
            
        is_gcd_one = (gcd_val == 1)
        
        # The conclusion Q is the equivalence of is_unit and is_gcd_one
        q = (is_unit == is_gcd_one)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: Z_n is the ring of integers modulo n",
    "¬Q: It is not the case that (a is a unit in Z_n if and only if gcd(a, n) == 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2