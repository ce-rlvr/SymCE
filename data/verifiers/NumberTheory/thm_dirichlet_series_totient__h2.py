import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import zeta
from sympy.ntheory import totient
import math

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: s is a complex number with Re(s) > 2
    try:
        s = complex(witness)
        h1 = s.real > 2
    except Exception:
        h1 = False

    # H_2: zeta(s) is the Riemann zeta function
    # This is a definitional hypothesis; it holds if s is a valid complex number.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The Dirichlet series for phi(n) does NOT converge absolutely to zeta(s-1)/zeta(s)
    try:
        if not h1:
            neg_q = False
        else:
            s_c = complex(witness)
            # Evaluate the exact analytical limit
            exact = complex(zeta(s_c - 1) / zeta(s_c))
            
            # Evaluate the partial sum up to N=2000 to ensure it runs under 5 seconds
            N = 2000
            partial_sum = sum(totient(n) / (n ** s_c) for n in range(1, N + 1))
            
            # The absolute error of the truncated series is strictly bounded by the integral 
            # of x^(1 - Re(s)) from N to infinity.
            if s_c.real > 2:
                error_bound = (N ** (2 - s_c.real)) / (s_c.real - 2)
            else:
                error_bound = float('inf')
            
            diff = abs(exact - partial_sum)
            
            # If the difference exceeds the mathematical error bound (plus a small float tolerance),
            # then the series does not converge to the expected value.
            if diff > error_bound + 1e-2:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: s is a complex number with Re(s) > 2",
    "H_2: zeta(s) is the Riemann zeta function",
    "¬Q: The Dirichlet series for phi(n) does not converge absolutely to zeta(s-1)/zeta(s)"
]

N_HYP = 2
NEG_Q_INDEX = 2