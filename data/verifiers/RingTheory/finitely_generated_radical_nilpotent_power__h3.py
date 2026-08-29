import sympy
from sympy import symbols
import math
import itertools
import functools

class InfinitePolynomialRingIdeal:
    """
    Represents an ideal I = (x_1^f(1), x_2^f(2), ...) in the commutative ring R = k[x_1, x_2, ...].
    The witness can be instantiated with a function f(i) that returns the exponent of x_i.
    For example: witness = InfinitePolynomialRingIdeal(lambda i: i)
    Alternatively, the witness can just be the callable `lambda i: i` itself.
    """
    def __init__(self, f):
        self.f = f

    def is_commutative_ring(self):
        return True

    def is_ideal(self):
        try:
            # Check that f returns positive integers for the first few variables
            return all(isinstance(self.f(i), int) and self.f(i) >= 1 for i in range(1, 20))
        except Exception:
            return False

    def radical_power_contained(self, k):
        # rad(I)^k is contained in I iff EVERY monomial of degree k is in I.
        # A monomial x_1^{d_1} ... x_m^{d_m} is in I iff d_j >= f(j) for some j.
        # It is NOT in I iff d_j <= f(j) - 1 for all j.
        # The maximum degree of a monomial NOT in I using the first 2000 variables is
        # the sum of (f(j) - 1) for j in 1..2000.
        # If this sum is >= k, we can form a monomial of degree k not in I.
        max_degree = 0
        for i in range(1, 2001):
            try:
                val = self.f(i)
                if not isinstance(val, int) or val < 1:
                    continue
                cap = val - 1
                if cap > 0:
                    max_degree += cap
                if max_degree >= k:
                    return False
            except Exception:
                pass
        return True

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: For all positive integers k, the k-th power of the radical of I is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Unpack tuple if the witness is provided as (R, I)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        witness = I

    # If the witness is just the exponent function, wrap it in our model
    if callable(witness):
        witness = InfinitePolynomialRingIdeal(witness)
        
    h1, h2, neg_q = False, False, False

    # 1. Try custom object interface (e.g., InfinitePolynomialRingIdeal)
    if hasattr(witness, 'is_commutative_ring') and hasattr(witness, 'is_ideal'):
        try:
            h1 = bool(witness.is_commutative_ring())
            h2 = bool(witness.is_ideal())
            
            # Check that for all k in 1..100, rad(I)^k is NOT contained in I
            neg_q = True
            for k in range(1, 101):
                if witness.radical_power_contained(k):
                    neg_q = False
                    break
        except Exception:
            pass
        return [h1, h2, neg_q]

    # 2. Try SymPy ideal interface (finite polynomial rings are Noetherian, so conclusion holds)
    try:
        if hasattr(witness, 'ring'):
            h1 = getattr(witness.ring, 'is_commutative', True)
            h2 = True
            neg_q = False
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Try list of SymPy expressions (finitely generated ideal, so conclusion holds)
    try:
        if isinstance(witness, list) and all(hasattr(g, 'free_symbols') for g in witness):
            h1 = True
            h2 = True
            neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]