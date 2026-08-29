import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Expected witness format: (n, I, J)
    where:
      - n is an integer >= 2, representing the commutative ring R = Z/nZ.
      - I is an iterable of integers representing a subset of R.
      - J is an iterable of integers representing an ideal of R.
    """
    try:
        n, I, J = witness
        if not isinstance(n, (int, sympy.Integer)) or n < 2:
            return [False, False, False, False]
        n = int(n)
        
        I_set = set(int(val) for val in I)
        J_set = set(int(val) for val in J)
        
        if not I_set.issubset(range(n)) or not J_set.issubset(range(n)):
            return [False, False, False, False]
            
        # H1: R is a commutative ring
        # Z/nZ is always a commutative ring for n >= 2
        h1 = True
        
        # H2: J is an ideal of R
        h2 = True
        if not J_set:
            h2 = False
        else:
            for a in J_set:
                for b in J_set:
                    if (a + b) % n not in J_set:
                        h2 = False
                for r in range(n):
                    if (a * r) % n not in J_set:
                        h2 = False
                        
        # H3: \sqrt{I} + \sqrt{J} = R
        # The radical of a subset is the radical of the ideal it generates.
        def get_ideal_rad(S):
            g = n
            for val in S:
                g = math.gcd(g, val)
            ideal_S = set((g * k) % n for k in range(n))
            rad = set()
            for val in range(n):
                curr = val
                for k in range(1, n + 2):
                    if curr in ideal_S:
                        rad.add(val)
                        break
                    curr = (curr * val) % n
            return rad
            
        rad_I = get_ideal_rad(I_set)
        rad_J = get_ideal_rad(J_set)
        
        rad_sum = set(((u + v) % n) for u in rad_I for v in rad_J)
        h3 = (len(rad_sum) == n)
        
        # Negated Conclusion: I + J != R
        # Since I is not necessarily an ideal, I + J is the Minkowski sum of the subsets.
        I_J_sum = set(((u + v) % n) for u in I_set for v in J_set)
        neg_q = (len(I_J_sum) != n)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: \\sqrt{I} + \\sqrt{J} = R",
    "¬Q: I + J != R"
]

N_HYP = 3
NEG_Q_INDEX = 3