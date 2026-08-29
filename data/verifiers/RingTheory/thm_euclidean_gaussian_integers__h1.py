import sympy
from sympy import *

class GaussianSubring:
    """
    Represents the ring Z[k*i] = {a + b*k*i | a, b in Z}.
    """
    def __init__(self, k):
        self.k = k

    def __str__(self):
        if self.k == 1:
            return "Z[i]"
        return f"Z[{self.k}i]"

# Common subrings of the Gaussian integers
Z_i = GaussianSubring(1)
Z_2i = GaussianSubring(2)
Z_3i = GaussianSubring(3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be an integer k >= 1 or a GaussianSubring(k),
    representing the ring R = Z[k*i].
    """
    try:
        if hasattr(witness, 'k'):
            k = int(witness.k)
        else:
            k = int(witness)
        h1 = (k >= 1)
    except Exception:
        return [False, False]
    
    try:
        # Check if R is a Euclidean domain with Euclidean function N(a+bi) = a^2+b^2.
        # We test a small grid of elements x, y in R.
        # For R to be Euclidean with N, for every x, y (y != 0), there must exist q in R
        # such that N(x - q*y) < N(y).
        is_euclidean = True
        for xa in range(-3, 4):
            for xb in range(-3, 4):
                for ya in range(-3, 4):
                    for yb in range(-3, 4):
                        if ya == 0 and yb == 0:
                            continue
                        
                        found_q = False
                        # Search for a quotient q = qa + qb*k*i
                        for qa in range(-5, 6):
                            for qb in range(-5, 6):
                                # x = xa + xb*k*i
                                # y = ya + yb*k*i
                                # q = qa + qb*k*i
                                # r = x - q*y
                                r_real = xa - qa*ya + qb*yb*k*k
                                r_imag_k = xb - qa*yb - qb*ya
                                
                                r_norm = r_real**2 + (r_imag_k * k)**2
                                y_norm = ya**2 + (yb * k)**2
                                
                                if r_norm < y_norm:
                                    found_q = True
                                    break
                            if found_q:
                                break
                        
                        if not found_q:
                            is_euclidean = False
                            break
                    if not is_euclidean:
                        break
                if not is_euclidean:
                    break
            if not is_euclidean:
                break
        
        neg_q = not is_euclidean
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N(a+bi) = a^2+b^2 is defined on R",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1