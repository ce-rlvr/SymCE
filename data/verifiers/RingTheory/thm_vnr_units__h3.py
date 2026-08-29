import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: Witness is a tuple/list (n, a) representing the ring Z/nZ and an element a
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, a = witness
            if isinstance(n, (int, sympy.Integer)) and isinstance(a, (int, sympy.Integer)) and n >= 2:
                n_int = int(n)
                a_int = int(a)
                
                # H_1: Check if Z/nZ is a von Neumann regular ring
                is_regular = True
                for x in range(n_int):
                    if not any((x * y * x) % n_int == x for y in range(n_int)):
                        is_regular = False
                        break
                h1 = is_regular
                
                # H_2: Check if a is an element of Z/nZ
                h2 = (0 <= a_int < n_int)
                
                # ¬Q: a is not a unit in Z/nZ
                neg_q = (math.gcd(a_int, n_int) != 1)
                
        # Case 2: Witness is a square matrix over a field (e.g., Rationals/Reals)
        elif hasattr(witness, 'is_square') and witness.is_square:
            # Matrix rings over fields are always von Neumann regular
            h1 = True
            h2 = True
            # A matrix is a unit iff its determinant is non-zero
            neg_q = bool(witness.det() == 0)
            
        # Case 3: Witness is a scalar in a field (e.g., Rational, Real)
        elif isinstance(witness, (int, float, sympy.Integer, sympy.Float, sympy.Rational)):
            # Fields are von Neumann regular rings
            h1 = True
            h2 = True
            # In a field, every element is a unit except 0
            neg_q = (witness == 0)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "H_2: a is an element of R",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2