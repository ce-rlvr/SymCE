import sympy
from sympy import MatrixBase, eye, zeros
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a ring with identity and a, b are elements of R, then 1 - ba is a unit."
    
    The witness can be provided as:
      - (a, b) for elements in a characteristic zero ring (like Z or matrices over Z)
      - (n, a, b) for elements in Z_n or matrices over Z_n, where n is an integer > 1.
    """
    try:
        modulus = None
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
                if isinstance(R, int) and R > 1:
                    modulus = R
            elif len(witness) == 2:
                a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a ring with identity
    try:
        if isinstance(a, MatrixBase):
            h1 = a.is_square
            one = eye(a.shape[0])
        else:
            h1 = True
            one = 1
    except Exception:
        h1 = False

    # H_2: a and b are elements of R
    try:
        if isinstance(a, MatrixBase):
            h2 = isinstance(b, MatrixBase) and a.shape == b.shape
        else:
            h2 = True
        
        # Verify that multiplication and subtraction are well-defined
        ba = b * a
        val = one - ba
        
        if modulus is not None:
            if isinstance(val, MatrixBase):
                val = val.applyfunc(lambda x: x % modulus)
            else:
                val = val % modulus
    except Exception:
        h2 = False

    # ¬Q: 1 - ba is NOT a unit in R
    try:
        if modulus is not None:
            if isinstance(val, MatrixBase):
                d = val.det() % modulus
                is_u = (math.gcd(int(d), modulus) == 1)
            else:
                is_u = (math.gcd(int(val), modulus) == 1)
        else:
            if isinstance(val, MatrixBase):
                d = val.det()
                if isinstance(d, float) or (hasattr(d, 'is_Float') and d.is_Float):
                    is_u = bool(d != 0)
                elif hasattr(d, 'is_Integer') and d.is_Integer:
                    is_u = (abs(d) == 1)
                elif isinstance(d, int):
                    is_u = (abs(d) == 1)
                elif hasattr(d, 'is_Rational') and d.is_Rational:
                    is_u = bool(d != 0)
                else:
                    is_u = bool(d != 0)
            else:
                if isinstance(val, float) or (hasattr(val, 'is_Float') and val.is_Float):
                    is_u = bool(val != 0)
                elif hasattr(val, 'is_Integer') and val.is_Integer:
                    is_u = (abs(val) == 1)
                elif isinstance(val, int):
                    is_u = (abs(val) == 1)
                elif hasattr(val, 'is_Rational') and val.is_Rational:
                    is_u = bool(val != 0)
                else:
                    is_u = bool(val != 0)
        neg_q = not is_u
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: a and b are elements of R",
    "¬Q: 1 - ba is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2