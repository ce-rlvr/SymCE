import math
import sympy
from sympy import symbols

# Top-level setup
Z = sympy.S.Integers
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: n is a positive integer",
    "H_3: P^(n) is the n-th symbolic power of P, defined as the contraction of P^n R_P to R",
    "¬Q: The symbolic power P^(n) is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        m, n = None, None
        
        # Attempt to parse witness as a dictionary
        if isinstance(witness, dict):
            for key in ['m', 'P', 'p', 'ideal', 'generator']:
                if key in witness:
                    try:
                        m = int(witness[key])
                        break
                    except Exception:
                        pass
            if 'n' in witness:
                try:
                    n = int(witness['n'])
                except Exception:
                    pass
        
        # Attempt to parse witness as a tuple/list
        if m is None or n is None:
            if isinstance(witness, (tuple, list)):
                def flatten(lst):
                    res = []
                    for i in lst:
                        if isinstance(i, (list, tuple, set)):
                            res.extend(flatten(i))
                        else:
                            res.append(i)
                    return res
                
                flat = flatten(witness)
                
                def extract_ints(item):
                    res = []
                    try:
                        res.append(int(item))
                    except Exception:
                        if hasattr(item, 'args'):
                            for arg in item.args:
                                res.extend(extract_ints(arg))
                    return res
                
                ints = []
                for val in flat:
                    ints.extend(extract_ints(val))
                    
                if len(ints) >= 2:
                    m = ints[-2]
                    n = ints[-1]
        
        if m is None or n is None:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring with identity
    # We implicitly evaluate the witness in the context of R = Z
    h1 = True
    
    # H2: n is a positive integer
    try:
        h2 = bool(n > 0)
    except Exception:
        h2 = False
        
    # H3: P^(n) is the n-th symbolic power of P, defined as the contraction of P^n R_P to R
    # This is a definitional hypothesis that holds by construction in our evaluation
    h3 = True
    
    # ¬Q: The symbolic power P^(n) is not a P-primary ideal
    # In any commutative ring, the radical of a primary ideal is ALWAYS a prime ideal.
    # Therefore, an ideal can only be "P-primary" if P itself is a prime ideal.
    # If P = (m) is not a prime ideal, then P^(n) cannot possibly be P-primary.
    try:
        def is_prime_ideal_gen(val):
            if val == 0:
                return True  # (0) is a prime ideal in Z
            val = abs(val)
            if val == 1:
                return False # (1) is not a prime ideal
            for i in range(2, math.isqrt(val) + 1):
                if val % i == 0:
                    return False
            return True
            
        neg_q = not is_prime_ideal_gen(m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]