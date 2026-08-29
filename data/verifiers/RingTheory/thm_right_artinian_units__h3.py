import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math

# Standard linear algebra objects that might be used as witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Attempt to convert lists of lists to a SymPy Matrix
        if isinstance(witness, list) and all(isinstance(row, list) for row in witness):
            try:
                witness = Matrix(witness)
            except Exception:
                pass

        if isinstance(witness, Matrix):
            # A square matrix over a field belongs to a matrix ring, which is right Artinian.
            if witness.is_square:
                h1 = True
                h2 = True
                # A matrix is a unit iff its determinant is non-zero
                neg_q = (witness.det() == 0)
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            # Interpret tuple (n, a) as element 'a' in the ring Z/nZ
            n, a = witness
            if isinstance(n, int) and isinstance(a, int) and n > 1:
                # Z/nZ is finite, hence Artinian
                h1 = True
                h2 = True
                # 'a' is a unit in Z/nZ iff gcd(a, n) == 1
                neg_q = (math.gcd(a, n) > 1)
                
        else:
            # Try to treat the witness as a number in a field (like Q, R, or C)
            # Fields are trivially right Artinian rings.
            expr = sympy.sympify(witness)
            if expr.is_zero:
                h1 = True
                h2 = True
                # 0 is never a unit in a field
                neg_q = True
            elif expr.is_zero is False:
                h1 = True
                h2 = True
                # Non-zero elements in a field are always units
                neg_q = False
                
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: a is an element of R",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2