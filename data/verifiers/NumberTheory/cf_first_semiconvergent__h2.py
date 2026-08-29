import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
        a = list(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: The sequence is a finite simple continued fraction
    try:
        h1 = True
        if len(a) < 1:
            h1 = False
        else:
            for i, x in enumerate(a):
                if not isinstance(x, (int, float, sympy.Integer)):
                    h1 = False
                    break
                if int(x) != x:
                    h1 = False
                    break
                if i > 0 and x < 1:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: p_{n-1}/q_{n-1} is the (n-1)-th convergent of the continued fraction
    try:
        h2 = h1
    except Exception:
        h2 = False

    # neg_Q: The simple continued fraction expansion of the rational number is NOT exactly the sequence appended with 1
    try:
        if not h1:
            neg_q = False
        else:
            p_prev, q_prev = 1, 0
            p_curr, q_curr = int(a[0]), 1
            
            p_n_minus_1, q_n_minus_1 = p_prev, q_prev
            
            for i in range(1, len(a)):
                p_n_minus_1, q_n_minus_1 = p_curr, q_curr
                p_next = int(a[i]) * p_curr + p_prev
                q_next = int(a[i]) * q_curr + q_prev
                p_prev, q_prev = p_curr, q_curr
                p_curr, q_curr = p_next, q_next
                
            p_n, q_n = p_curr, q_curr
            
            num = p_n + p_n_minus_1
            den = q_n + q_n_minus_1
            
            if den == 0:
                neg_q = False
            else:
                n, d = num, den
                if d < 0:
                    n, d = -n, -d
                cf = []
                while d != 0:
                    q = n // d
                    cf.append(q)
                    n, d = d, n - q * d
                
                # Standardize the continued fraction (last term should be >= 2 unless it's exactly length 1)
                if len(cf) > 1 and cf[-1] == 1:
                    cf[-2] += 1
                    cf.pop()
                    
                expected = [int(x) for x in a] + [1]
                neg_q = (cf != expected)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The sequence is a finite simple continued fraction",
    "H_2: p_n-1 / q_n-1 is the n-1 th convergent",
    "¬Q: The continued fraction expansion is NOT the sequence appended with 1"
]

N_HYP = 2
NEG_Q_INDEX = 2