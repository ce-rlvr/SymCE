import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I has a primary decomposition I = \\bigcap_{i=1}^n Q_i",
    "H_3: J is an ideal in R",
    "¬Q: The ideal quotient (I:J) is not equal to the intersection \\bigcap_{i=1}^n (Q_i:J)"
]

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a tuple (I_val, Q_vals, J_val) representing ideals in the integers Z.
    I_val: int
    Q_vals: list of ints
    J_val: int
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        I_val, Q_vals, J_val = witness
        
        I_val = int(I_val)
        J_val = int(J_val)
        Q_vals = [int(q) for q in Q_vals]
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    # The ring of integers Z is always a commutative ring.
    h1 = True

    # H2: I has a primary decomposition I = \bigcap_{i=1}^n Q_i
    try:
        if len(Q_vals) == 0:
            h2 = False
        else:
            # Intersection of ideals in Z corresponds to the LCM of their generators
            intersection = Q_vals[0]
            for q in Q_vals[1:]:
                if intersection == 0 or q == 0:
                    intersection = 0
                else:
                    intersection = abs(intersection * q) // math.gcd(intersection, q)
            
            is_intersection = (abs(I_val) == abs(intersection))
            
            # Check if each Q_i is a primary ideal in Z
            # In Z, (q) is primary iff q = 0 or q = p^k for some prime p and k >= 1
            all_primary = True
            for q in Q_vals:
                if q == 0:
                    continue
                if abs(q) == 1:
                    all_primary = False
                    break
                factors = sympy.factorint(abs(q))
                if len(factors) > 1:
                    all_primary = False
                    break
            
            h2 = is_intersection and all_primary
    except Exception:
        h2 = False

    # H3: J is an ideal in R
    # Any integer generates an ideal in Z.
    h3 = True

    # neg_Q: (I:J) != \bigcap_{i=1}^n (Q_i:J)
    try:
        def ideal_quotient(a, b):
            a = abs(a)
            b = abs(b)
            if a == 0:
                if b == 0:
                    return 1  # (0:0) = Z = (1)
                else:
                    return 0  # (0:b) = (0) for b != 0
            else:
                if b == 0:
                    return 1  # (a:0) = Z = (1)
                else:
                    return a // math.gcd(a, b)

        I_colon_J = ideal_quotient(I_val, J_val)
        
        q_colon_j_vals = [ideal_quotient(q, J_val) for q in Q_vals]
        
        if len(q_colon_j_vals) == 0:
            rhs = 1
        else:
            rhs = q_colon_j_vals[0]
            for q in q_colon_j_vals[1:]:
                if rhs == 0 or q == 0:
                    rhs = 0
                else:
                    rhs = abs(rhs * q) // math.gcd(rhs, q)
        
        neg_q = (abs(I_colon_J) != abs(rhs))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]