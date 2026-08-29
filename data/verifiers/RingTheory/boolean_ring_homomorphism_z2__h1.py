import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be either:
      - An integer or matrix `x`, implying the ring R is Z or M_k(Z).
      - A tuple `(n, x)` where `n` is the modulus of Z/nZ (n=0 means Z) 
        and `x` is an element (integer or matrix) in that ring.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, x = witness
        else:
            n = 0
            x = witness
            
        n = abs(int(n))
        
        if isinstance(x, sympy.Matrix):
            if n == 1:
                h1 = False
            else:
                if n == 0:
                    h1 = not x.is_zero_matrix
                else:
                    h1 = any(int(val) % n != 0 for val in x)
        else:
            x = int(x)
            if n == 0:
                h1 = (x != 0)
            elif n == 1:
                h1 = False
            else:
                h1 = (x % n != 0)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, x = witness
        else:
            n = 0
            x = witness
            
        n = abs(int(n))
        
        if isinstance(x, sympy.Matrix):
            # There is no ring homomorphism from M_k(R) to Z/2Z for k >= 2.
            if x.shape[0] >= 2:
                q = False
            else:
                val = int(x[0, 0])
                if n % 2 == 0:
                    q = (val % 2 == 1)
                else:
                    q = False
        else:
            x = int(x)
            # A ring homomorphism f: Z/nZ -> Z/2Z exists iff n is even or n=0.
            # If it exists, it is unique and given by f(a) = a mod 2.
            if n % 2 == 0:
                q = (x % 2 == 1)
            else:
                q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a non-zero element of R",
    "¬Q: There is no ring homomorphism f: R -> Z/2Z such that f(x) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1