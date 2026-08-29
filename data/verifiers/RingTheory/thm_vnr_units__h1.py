import sympy as sp
import math
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        a = witness
        
        # If witness explicitly specifies a finite ring Z_n as a tuple (n, a)
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, a = witness
            if isinstance(ring, int) and ring > 1:
                h1 = True
                val = int(a) % ring
                # In Z_n, an element is not a zero-divisor iff it is coprime to n
                h2 = (math.gcd(val, ring) == 1)
                # In Z_n, an element is a unit iff it is coprime to n
                q = (math.gcd(val, ring) == 1)
                neg_q = not q
                return [h1, h2, neg_q]
            
        # Evaluate in Z
        if isinstance(a, (int, sp.Integer)):
            h1 = True
            val = int(a)
            h2 = (val != 0)
            q = (abs(val) == 1)
            neg_q = not q
            
        # Evaluate in R (Field)
        elif isinstance(a, float):
            h1 = True
            h2 = (a != 0.0)
            q = (a != 0.0)
            neg_q = not q
            
        # Evaluate in Q (Field)
        elif isinstance(a, sp.Rational) and not isinstance(a, sp.Integer):
            h1 = True
            h2 = (a != 0)
            q = (a != 0)
            neg_q = not q
            
        # Evaluate in M_n(Z) or M_n(Q)
        elif isinstance(a, sp.Matrix):
            if a.is_square:
                h1 = True
                det = a.det()
                h2 = (det != 0)
                # If all entries are integers, it's in M_n(Z), where units have determinant ±1
                if all(isinstance(val, (int, sp.Integer)) for val in a):
                    q = (abs(det) == 1)
                else:
                    q = (det != 0)
                neg_q = not q
                
        # Evaluate in Z[x, y, z]
        elif isinstance(a, sp.Expr):
            h1 = True
            simplified = sp.simplify(a)
            h2 = (simplified != 0)
            q = (simplified in [1, -1, sp.Integer(1), sp.Integer(-1)])
            neg_q = not q
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "H_2: a is not a zero-divisor in R",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2