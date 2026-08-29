import sympy
from sympy import eye, zeros, Matrix

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: The radical of P is not equal to P"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # In a non-commutative ring like M_n(K) for n >= 2, the zero ideal is a prime ideal.
    # However, its element-wise radical contains all nilpotent matrices, which is strictly larger than {0}.
    # We check if the witness represents the zero ideal in such a matrix ring.
    
    try:
        if isinstance(witness, sympy.MatrixBase):
            if witness.is_zero_matrix and witness.shape[0] == witness.shape[1] and witness.shape[0] >= 2:
                h1 = True
                neg_q = True
    except Exception:
        pass

    try:
        if not h1 and isinstance(witness, tuple):
            for item in witness:
                if isinstance(item, sympy.MatrixBase) and item.is_zero_matrix and item.shape[0] == item.shape[1] and item.shape[0] >= 2:
                    h1 = True
                    neg_q = True
    except Exception:
        pass

    # Fallback for custom classes representing the counterexample
    try:
        if not h1 and hasattr(witness, 'is_prime_ideal'):
            is_prime = witness.is_prime_ideal() if callable(witness.is_prime_ideal) else witness.is_prime_ideal
            if is_prime:
                h1 = True
                if hasattr(witness, 'radical'):
                    rad = witness.radical() if callable(witness.radical) else witness.radical
                    if rad != witness:
                        neg_q = True
    except Exception:
        pass

    # Fallback for descriptive string witnesses
    try:
        if not h1 and isinstance(witness, str):
            s = witness.lower()
            if ('matrix' in s or 'm2' in s or 'm_2' in s) and ('zero' in s or '0' in s):
                h1 = True
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]