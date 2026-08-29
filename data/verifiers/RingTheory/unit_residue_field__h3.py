import sympy
import math
from sympy import eye, zeros
from sympy.abc import t, x, y

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a tuple: (n, p, x)
    where:
      n is an integer >= 2, representing the ring R = Z/nZ
      p is a prime, representing the maximal ideal m = (p)
      x is an element (could be an integer, a polynomial, a matrix, etc.)
    """
    try:
        n, p, x_val = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    # Z/nZ is a commutative ring for any integer n >= 2
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False

    # H_2: R is a local ring with maximal ideal m
    # Z/nZ is a local ring iff n is a prime power p^k (k >= 1)
    try:
        h2 = False
        if isinstance(p, int) and sympy.isprime(p):
            temp = n
            while temp % p == 0 and temp > 0:
                temp //= p
            if temp == 1 and n > 1:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: x is a unit in R iff the image of x in R/m is non-zero (fails)
    try:
        # Evaluate "x is a unit in R"
        # Only elements actually in R (integers mod n) can be units in R.
        if isinstance(x_val, int):
            is_unit_R = (math.gcd(x_val, n) == 1)
        elif hasattr(x_val, 'is_Integer') and x_val.is_Integer:
            is_unit_R = (math.gcd(int(x_val), n) == 1)
        else:
            is_unit_R = False

        # Evaluate "image of x in R/m is non-zero"
        # R/m is isomorphic to Z/pZ.
        if isinstance(x_val, int):
            image_nonzero = (x_val % p) != 0
        elif hasattr(x_val, 'is_Integer') and x_val.is_Integer:
            image_nonzero = (int(x_val) % p) != 0
        elif isinstance(x_val, sympy.MatrixBase):
            image_nonzero = any((int(e) % p) != 0 for e in x_val)
        elif isinstance(x_val, (list, tuple)):
            image_nonzero = any((int(e) % p) != 0 for e in x_val)
        elif isinstance(x_val, sympy.Expr):
            # For polynomials or other symbolic expressions
            poly = sympy.Poly(x_val, domain=sympy.GF(p))
            image_nonzero = not poly.is_zero
        else:
            image_nonzero = False

        q = (is_unit_R == image_nonzero)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "¬Q: x is not a unit in R but its image in R/m is non-zero (or vice versa)"
]

N_HYP = 2
NEG_Q_INDEX = 2