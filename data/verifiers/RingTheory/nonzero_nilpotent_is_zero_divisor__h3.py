import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals
R_reals = S.Reals
C = S.Complexes

class IntegersModRing:
    """A simple implementation of the ring of integers modulo n."""
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
        self.is_commutative = True

    def __contains__(self, x):
        return x in self.elements

    def add(self, x, y):
        return (x + y) % self.n

    def mul(self, x, y):
        return (x * y) % self.n

    def is_zero_divisor(self, x):
        if x not in self:
            return False
        for y in self.elements:
            if y != self.zero and self.mul(x, y) == self.zero:
                return True
        return False

    def __str__(self):
        return f"Z_{self.n}"

# Provide some finite rings in case the witness uses them
Z4_ring = IntegersModRing(4)
Z6_ring = IntegersModRing(6)
Z8_ring = IntegersModRing(8)


def conditions(witness) -> list[bool]:
    """
    Given a witness (R, x), checks if it is a valid counterexample to the false conjecture:
    "In a commutative ring R, any non-zero element x is a zero divisor."
    """
    try:
        R, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    try:
        h1 = False
        if isinstance(R, sympy.polys.domains.Domain):
            h1 = True
        elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'elements') and hasattr(R, 'mul'):
            h1 = True
            for a in R.elements:
                for b in R.elements:
                    if R.mul(a, b) != R.mul(b, a):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: x is a non-zero element of R
    try:
        h2 = False
        if h1:
            zero = R.zero if hasattr(R, 'zero') else 0
            if x in R or (hasattr(R, 'of_type') and R.of_type(x)):
                if x != zero and x != 0:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: x is NOT a zero divisor in R
    try:
        neg_q = False
        if h1 and h2:
            is_zd = False
            if hasattr(R, 'is_zero_divisor'):
                is_zd = R.is_zero_divisor(x)
            elif hasattr(R, 'elements') and hasattr(R, 'mul'):
                zero = R.zero if hasattr(R, 'zero') else 0
                for y in R.elements:
                    if y != zero and R.mul(x, y) == zero:
                        is_zd = True
                        break
            elif isinstance(R, sympy.polys.domains.Domain):
                # Standard SymPy domains (ZZ, QQ, RR, CC, etc.) are integral domains
                is_zd = False
            elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
                is_zd = False
            
            neg_q = not is_zd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]


CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is a non-zero element of R",
    "¬Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2