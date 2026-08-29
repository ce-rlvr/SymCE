import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypothesis: Let N(a+bω) = a^2-ab+b^2 be the norm function defined on R
    Conclusion: R is a Euclidean domain with Euclidean function N
    """
    
    def get_in_R(w):
        if callable(w):
            return lambda a, b: bool(w(a, b))
        elif hasattr(w, '__contains__'):
            return lambda a, b: (a, b) in w
        elif isinstance(w, int):
            if w == 0:
                return lambda a, b: b == 0
            else:
                return lambda a, b: b % w == 0
        else:
            return lambda a, b: False

    in_R = get_in_R(witness)
    
    def norm(a, b):
        return a**2 - a*b + b**2

    # H_1: N(a+bω) = a^2-ab+b^2 is defined on R
    # We verify this by checking if R is a valid subring of Z[ω]
    try:
        h1_ok = False
        if in_R(0, 0) and in_R(1, 0):
            elements = []
            # Add some specific elements if witness is an integer to ensure we test b != 0
            if isinstance(witness, int) and witness != 0:
                c = abs(witness)
                for a in [0, c, -c, 1, -1]:
                    for b in [0, c, -c, 1, -1]:
                        if in_R(a, b) and (a, b) not in elements:
                            elements.append((a, b))
                            
            # Add standard small elements
            for a in range(-5, 6):
                for b in range(-5, 6):
                    if in_R(a, b) and (a, b) not in elements:
                        elements.append((a, b))
            
            if elements:
                closure_ok = True
                for e1 in elements:
                    for e2 in elements:
                        # Check closure under addition and subtraction
                        if not in_R(e1[0] + e2[0], e1[1] + e2[1]): 
                            closure_ok = False
                            break
                        if not in_R(e1[0] - e2[0], e1[1] - e2[1]): 
                            closure_ok = False
                            break
                        # Check closure under multiplication in Z[ω]
                        # (a1 + b1 ω)(a2 + b2 ω) = (a1 a2 - b1 b2) + (a1 b2 + a2 b1 - b1 b2)ω
                        p_a = e1[0]*e2[0] - e1[1]*e2[1]
                        p_b = e1[0]*e2[1] + e1[1]*e2[0] - e1[1]*e2[1]
                        if not in_R(p_a, p_b): 
                            closure_ok = False
                            break
                    if not closure_ok:
                        break
                h1_ok = closure_ok
    except Exception:
        h1_ok = False

    # ¬Q: R is NOT a Euclidean domain with Euclidean function N
    # We search for A, B in R (B != 0) such that for ALL Q in R, N(A - BQ) >= N(B)
    try:
        neg_q_ok = False
        elements = []
        if isinstance(witness, int) and witness != 0:
            c = abs(witness)
            for a in [0, c, -c, 1, -1, 2, -2]:
                for b in [0, c, -c, 1, -1, 2, -2]:
                    if in_R(a, b) and (a, b) not in elements:
                        elements.append((a, b))
                        
        for a in range(-10, 11):
            for b in range(-10, 11):
                if in_R(a, b) and (a, b) not in elements:
                    elements.append((a, b))
                    
        for A in elements:
            for B in elements:
                if B == (0, 0):
                    continue
                
                NB = norm(B[0], B[1])
                # Compute A/B = x + y ω in the field of fractions Q(ω)
                x = (A[0]*B[0] - A[0]*B[1] + A[1]*B[1]) / NB
                y = (A[1]*B[0] - A[0]*B[1]) / NB
                
                found_Q = False
                # The required Q = q1 + q2 ω must be geometrically close to A/B
                # N(A/B - Q) < 1 implies |x - q1| < 1.16 and |y - q2| < 1.16
                min_q1 = int(math.floor(x)) - 2
                max_q1 = int(math.floor(x)) + 3
                min_q2 = int(math.floor(y)) - 2
                max_q2 = int(math.floor(y)) + 3
                
                for q1 in range(min_q1, max_q1):
                    for q2 in range(min_q2, max_q2):
                        if in_R(q1, q2):
                            # Compute remainder A - BQ exactly in integers
                            rem_a = A[0] - B[0]*q1 + B[1]*q2
                            rem_b = A[1] - B[0]*q2 - B[1]*q1 + B[1]*q2
                            if norm(rem_a, rem_b) < NB:
                                found_Q = True
                                break
                    if found_Q:
                        break
                
                if not found_Q:
                    # Found a pair (A, B) that cannot be divided with a smaller remainder
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N(a+bω) = a^2-ab+b^2 is defined on R",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1