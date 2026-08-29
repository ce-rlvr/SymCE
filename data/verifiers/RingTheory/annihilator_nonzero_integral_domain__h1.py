import sympy
from sympy import Matrix, eye, zeros
import math

# Standard algebra objects for linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If x is a non-zero element of R, then the annihilator ideal of x in R is {0}."
    (The hypothesis that R is an integral domain was dropped).
    
    The witness can be:
      - A tuple (n, x) representing the element x in the ring Z/nZ.
      - A square sympy Matrix representing an element in the ring of n x n matrices.
      - An integer representing an element in Z.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, x = witness
            n = int(n)
            x = int(x)
            if n > 1:
                h1 = (x % n != 0)
                # In Z/nZ, the annihilator of x is non-zero iff gcd(x, n) > 1
                neg_q = (math.gcd(x, n) > 1)
                
        elif hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            if witness.rows == witness.cols and witness.rows > 0:
                h1 = not witness.is_zero_matrix
                # In a matrix ring over a field or domain, an element has a non-zero 
                # annihilator (i.e. is a zero divisor) iff its determinant is 0.
                neg_q = (witness.det() == 0)
                
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = (witness != 0)
            # In the integral domain Z, the annihilator of any non-zero element is {0}.
            neg_q = False
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a non-zero element of R",
    "¬Q: The annihilator ideal of x in R is not the zero ideal {0}"
]

N_HYP = 1
NEG_Q_INDEX = 1