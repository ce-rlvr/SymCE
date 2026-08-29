import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import math

# Standard algebra objects relevant to RingTheory
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Witness can be a tuple (R, x) or just R (in which case we find an x)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R_obj, x_obj = witness
        else:
            R_obj = witness
            x_obj = None
            
        # Handle infinite domains/fields
        if R_obj in (ZZ, QQ, RR, CC):
            h1 = True
            if x_obj is None:
                x_val = 2
            else:
                x_val = x_obj
            h2 = (x_val != 0 and x_val != 1)
            # In integral domains/fields, no non-zero element is a zero divisor
            neg_q = (x_val != 0)
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Handle finite rings Z_n
        if hasattr(R_obj, 'mod'):
            n = int(R_obj.mod)
        else:
            n = int(R_obj)
            
        if x_obj is not None:
            x_val = int(x_obj) % n
        else:
            x_val = None
            # Try to find an element x that is not a zero divisor (i.e. coprime to n)
            for i in range(2, n):
                if math.gcd(i, n) == 1:
                    x_val = i
                    break
            if x_val is None:
                x_val = 0
                
        h1 = (n > 2)
        h2 = (x_val != 0 and x_val != 1)
        # In Z_n, an element is NOT a zero divisor if and only if it is coprime to n
        neg_q = (math.gcd(x_val, n) == 1)
        
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The cardinality of R is strictly greater than 2",
    "H_2: x is a non-zero element of R such that x != 1",
    "¬Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2