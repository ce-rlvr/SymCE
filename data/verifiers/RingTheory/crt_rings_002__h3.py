import sympy
from sympy import symbols, Integer, lcm, expand, simplify
import math

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        # Witness can be (I, J) or (R, I, J)
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                I, J = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Case 1: Ideals in Z, represented by integer generators
        if isinstance(I, (int, Integer)) and isinstance(J, (int, Integer)):
            H1 = True
            H2 = True
            i_val = int(I)
            j_val = int(J)
            
            if i_val == 0 and j_val == 0:
                cap = 0
            else:
                cap = abs(i_val * j_val) // math.gcd(i_val, j_val)
                
            prod = abs(i_val * j_val)
            neg_Q = (cap != prod)
            
        # Case 2: Principal ideals in a polynomial ring, represented by sympy expressions
        elif hasattr(I, 'free_symbols') and hasattr(J, 'free_symbols'):
            H1 = True
            H2 = True
            cap = lcm(I, J)
            prod = expand(I * J)
            
            if prod == 0:
                neg_Q = (cap != 0)
            else:
                ratio = simplify(cap / prod)
                # If they generate the same ideal, their ratio is a unit (constant)
                neg_Q = not (ratio.is_number and ratio != 0)
                
    except Exception:
        pass
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "¬Q: I \\cap J \\neq IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2