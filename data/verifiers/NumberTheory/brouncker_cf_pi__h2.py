import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, B = witness
        else:
            B = witness
            A = lambda n: (2*n - 1)**2
    except Exception:
        return [False, False]

    # H_1: A_n = (2n-1)^2 for n >= 1
    h1_ok = True
    try:
        for n in range(1, 1001):
            if int(A(n)) != (2*n - 1)**2:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: The continued fraction does not converge to 4/pi
    neg_q_ok = False
    try:
        P_prev, P_curr = 1, 1
        Q_prev, Q_curr = 0, 1
        
        for n in range(1, 1001):
            a = int(A(n))
            b = int(B(n))
            P_next = b * P_curr + a * P_prev
            Q_next = b * Q_curr + a * Q_prev
            P_prev, P_curr = P_curr, P_next
            Q_prev, Q_curr = Q_curr, Q_next
            
        target = 4.0 / math.pi
        # We check if the last two convergents are within 0.02 of 4/pi.
        # Using integer arithmetic to avoid float overflow with huge numbers.
        L = int(1000000 * (target - 0.02))
        U = int(1000000 * (target + 0.02))
        
        converges_to_target = True
        for P, Q in [(P_curr, Q_curr), (P_prev, Q_prev)]:
            if Q == 0:
                converges_to_target = False
                break
            if Q < 0:
                P, Q = -P, -Q
            if not (L * Q <= 1000000 * P <= U * Q):
                converges_to_target = False
                break
                
        neg_q_ok = not converges_to_target
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The sequence of partial numerators is given by A_n = (2n-1)^2 for n >= 1",
    "¬Q: The general continued fraction does not converge to 4/pi"
]

N_HYP = 1
NEG_Q_INDEX = 1