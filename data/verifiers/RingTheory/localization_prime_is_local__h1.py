import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_zero_ideal(P):
    if P == 0:
        return True
    try:
        if P.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if P.is_zero:
            return True
    except Exception:
        pass
    return False

class MatrixRingOverField:
    """
    Represents the ring of n x n matrices over a field F.
    """
    def __init__(self, n):
        self.n = n

    def has_multiplicative_identity(self):
        return True

    def is_prime_ideal(self, P):
        # In M_n(F), the only two-sided ideals are (0) and M_n(F).
        # (0) is a prime ideal.
        return _is_zero_ideal(P)

    def localization_is_local_ring(self, P):
        # The localization of M_n(F) at the prime ideal P=0
        # is M_n(F) itself.
        # A ring is local if the set of its non-units forms an ideal.
        # In M_n(F), non-units are singular matrices. For n > 1, the sum of 
        # two singular matrices can be invertible, so they do not form an ideal.
        # Thus, M_n(F) is local iff n == 1.
        if _is_zero_ideal(P):
            return self.n == 1
        return False

class Z_ring:
    """Represents the commutative ring of integers."""
    def has_multiplicative_identity(self):
        return True
        
    def is_prime_ideal(self, P):
        if _is_zero_ideal(P):
            return True
        try:
            return sympy.isprime(P)
        except Exception:
            return False
        
    def localization_is_local_ring(self, P):
        if _is_zero_ideal(P):
            return True
        try:
            if sympy.isprime(P):
                return True
        except Exception:
            pass
        return False

M2 = MatrixRingOverField(2)
M3 = MatrixRingOverField(3)
ZZ = Z_ring()
P_zero = 0

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (R, P), checks if it satisfies the remaining hypotheses
    and fails the conclusion.
    """
    try:
        R, P = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = bool(R.has_multiplicative_identity())
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(R.is_prime_ideal(P))
    except Exception:
        h2_ok = False
        
    try:
        # neg_Q is True if the conclusion FAILS (i.e., localization is NOT a local ring)
        neg_q_ok = not bool(R.localization_is_local_ring(P))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: P is a prime ideal of R",
    "¬Q: The localization R_P is not a local ring with unique maximal ideal PR_P"
]

N_HYP = 2
NEG_Q_INDEX = 2