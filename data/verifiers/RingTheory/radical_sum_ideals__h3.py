import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class FiniteRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n
        
    def __repr__(self):
        return f"Z_{self.n}"

# Standard finite rings for witness construction
Z2 = FiniteRing(2)
Z3 = FiniteRing(3)
Z4 = FiniteRing(4)
Z6 = FiniteRing(6)
Z8 = FiniteRing(8)
Z12 = FiniteRing(12)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    try:
        # Parse witness
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('n'))
            I = witness.get('I')
            J = witness.get('J')
        elif hasattr(witness, 'R'):
            R = witness.R
            I = witness.I
            J = witness.J
        elif hasattr(witness, 'n'):
            R = witness.n
            I = witness.I
            J = witness.J
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False]

        I = set(I)
        J = set(J)

        # Setup ring operations
        if isinstance(R, int):
            n = R
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
            h1 = (n >= 1)
        elif hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul') and hasattr(R, 'zero'):
            elements = list(R.elements)
            add = R.add
            mul = R.mul
            zero = R.zero
            is_comm = all(mul(a, b) == mul(b, a) for a in elements for b in elements)
            has_zero = zero in elements
            h1 = is_comm and has_zero
        else:
            return [False, False, False]

        # Check if I is an ideal
        if I and zero in I:
            closed_add = all(add(a, b) in I for a in I for b in I)
            closed_mul = all(mul(r, a) in I for r in elements for a in I)
            h2 = closed_add and closed_mul
        else:
            h2 = False

        # Helper to compute the radical of a subset in a finite ring
        def radical(S):
            rad_S = set()
            for x in elements:
                curr = x
                found = False
                # In a finite ring of size N, the sequence x, x^2, x^3... is periodic.
                # Checking powers up to N is sufficient to find if x^k in S.
                for _ in range(len(elements)):
                    if curr in S:
                        found = True
                        break
                    curr = mul(curr, x)
                if found:
                    rad_S.add(x)
            return rad_S

        # Helper to compute the Minkowski sum of two subsets
        def set_add(S1, S2):
            if not S1 or not S2:
                return set()
            return set(add(a, b) for a in S1 for b in S2)

        # Evaluate conclusion
        I_plus_J = set_add(I, J)
        rad_I = radical(I)
        rad_J = radical(J)
        rad_I_plus_rad_J = set_add(rad_I, rad_J)

        rad_I_plus_J = radical(I_plus_J)
        rad_rad_I_plus_rad_J = radical(rad_I_plus_rad_J)

        neg_q = (rad_I_plus_J != rad_rad_I_plus_rad_J)

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The radical of I + J is not equal to the radical of \\sqrt{I} + \\sqrt{J}"
]

N_HYP = 2
NEG_Q_INDEX = 2