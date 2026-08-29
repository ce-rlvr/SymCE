import math
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Case 1: Witness is a matrix (representing an element in M_n(R))
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            I = eye(witness.shape[0])
            try:
                h1 = witness.det() != 0
            except Exception:
                h1 = False
            h2 = bool(witness**2 == I)
            neg_q = bool(witness != I and witness != -I)
            return [bool(h1), h2, neg_q]
            
        # Case 2: Witness is a tuple (u, n) representing u in Z_n
        if isinstance(witness, tuple) and len(witness) == 2:
            u_val, n = int(witness[0]), int(witness[1])
            if n > 1:
                h1 = math.gcd(u_val, n) == 1
                h2 = (u_val**2) % n == 1
                neg_q = (u_val % n != 1) and (u_val % n != (-1) % n)
                return [bool(h1), bool(h2), bool(neg_q)]
                
        # Case 3: Witness is a scalar
        try:
            h1 = bool(witness != 0)
            h2 = bool(witness**2 == 1)
            neg_q = bool(witness != 1 and witness != -1)
            return [h1, h2, neg_q]
        except Exception:
            pass

    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: u is a unit in R",
    "H_2: u^2 = 1",
    "¬Q: u != 1 and u != -1"
]

N_HYP = 2
NEG_Q_INDEX = 2