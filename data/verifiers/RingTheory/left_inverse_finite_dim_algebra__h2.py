import sympy
from sympy import eye, zeros
import itertools
import functools
import math

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class PolyShift:
    """
    Represents an element in the Toeplitz algebra k<S, S*> / (S* S - 1).
    This is the standard counterexample algebra for infinite-dimensional vector spaces
    (e.g., the algebra of bounded linear operators on l^2 with the unilateral shift).
    Basis elements are of the form S^i (S*)^j, represented by the tuple (i, j).
    """
    def __init__(self, terms):
        self.terms = {}
        for (i, j), c in terms.items():
            if c != 0:
                self.terms[(i, j)] = self.terms.get((i, j), 0) + c
                if self.terms[(i, j)] == 0:
                    del self.terms[(i, j)]
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = PolyShift({(0, 0): other})
        res = dict(self.terms)
        for (i, j), c in other.terms.items():
            res[(i, j)] = res.get((i, j), 0) + c
            if res[(i, j)] == 0:
                del res[(i, j)]
        return PolyShift(res)

    def __radd__(self, other):
        return self.__add__(other)
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = PolyShift({(0, 0): other})
        res = {}
        for (i1, j1), c1 in self.terms.items():
            for (i2, j2), c2 in other.terms.items():
                c = c1 * c2
                # Apply the relation (S*)^j1 S^i2 = S^(i2 - j1) if j1 <= i2
                # or (S*)^(j1 - i2) if j1 > i2
                if j1 <= i2:
                    i = i1 + i2 - j1
                    j = j2
                else:
                    i = i1
                    j = j2 + j1 - i2
                res[(i, j)] = res.get((i, j), 0) + c
                if res[(i, j)] == 0:
                    del res[(i, j)]
        return PolyShift(res)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            other = PolyShift({(0, 0): other})
            return other.__mul__(self)
        return NotImplemented
        
    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = PolyShift({(0, 0): other})
        if not isinstance(other, PolyShift):
            return False
        return self.terms == other.terms

# Pre-defined elements for the witness
x_shift = PolyShift({(1, 0): 1})  # The unilateral right shift S
y_shift = PolyShift({(0, 1): 1})  # The unilateral left shift S*
one_shift = PolyShift({(0, 0): 1}) # The identity operator

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (x, y, one), checks if it is a valid counterexample.
    """
    try:
        x, y, one = witness
    except Exception:
        return [False, False]
    
    # Hypothesis 1: yx = 1 (x has a left inverse y)
    try:
        h1_ok = bool(y * x == one)
    except Exception:
        h1_ok = False
        
    # Negated Conclusion: x is NOT a unit with unique two-sided inverse y.
    # If xy != 1, then y is not a right inverse, so the conclusion fails.
    try:
        neg_q_ok = bool(x * y != one)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: yx = 1 (x has a left inverse y)",
    "¬Q: xy != 1 (x is not a unit / y is not a two-sided inverse)"
]

N_HYP = 1
NEG_Q_INDEX = 1