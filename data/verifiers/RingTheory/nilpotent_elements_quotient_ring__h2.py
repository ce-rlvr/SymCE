import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness: (m, I, x)
    m: int >= 2, representing the commutative ring R = Z/mZ
    I: list of int, representing a subset of R
    x: int, representing an element of R
    """
    try:
        m, I_list, x = witness
        m = int(m)
        if m < 2 or m > 1000:
            return [False, False, False]
        I = set(int(i) % m for i in I_list)
        x = int(x) % m
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    # Z/mZ is a commutative ring for any m >= 2
    try:
        h1 = (m >= 2)
    except Exception:
        h1 = False

    # H_2: x is an element of R
    # x is reduced modulo m, so it is always in R
    try:
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    try:
        # Check if I is an ideal of R
        is_ideal = True
        if 0 not in I:
            is_ideal = False
        else:
            for a in I:
                for b in I:
                    if (a - b) % m not in I:
                        is_ideal = False
                for r in range(m):
                    if (a * r) % m not in I:
                        is_ideal = False

        # RHS of conclusion: exists n >= 1 such that x^n \in I
        rhs = False
        curr = x
        for n in range(1, m + 2):
            if curr in I:
                rhs = True
                break
            curr = (curr * x) % m

        # LHS of conclusion: x + I is a nilpotent element in the quotient ring R/I
        # If I is not an ideal, R/I is not a quotient ring, so LHS is False.
        if is_ideal:
            lhs = rhs
        else:
            lhs = False

        # The conclusion is the equivalence LHS <-> RHS
        conclusion = (lhs == rhs)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is an element of R",
    "¬Q: The equivalence fails (e.g. R/I is not a quotient ring but x^n in I)"
]

N_HYP = 2
NEG_Q_INDEX = 2