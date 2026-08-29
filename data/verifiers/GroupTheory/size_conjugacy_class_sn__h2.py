import math
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        n, C, m = witness
    except Exception:
        return [False, False, False]

    # H1: n is a positive integer
    try:
        h1_ok = type(n) is int and n > 0
    except Exception:
        h1_ok = False

    # H2: The elements of C have a disjoint cycle decomposition consisting of exactly m_k cycles of length k for each 1 <= k <= n
    try:
        h2_ok = True
        if not hasattr(C, '__iter__'):
            h2_ok = False
        else:
            C_list = list(C)
            for p in C_list:
                if not isinstance(p, Permutation):
                    h2_ok = False
                    break
                
                # Check if permutation is valid in S_n
                if any(x >= n for x in p.support()):
                    h2_ok = False
                    break
                
                struct = p.cycle_structure
                for k in range(1, n + 1):
                    if k == 1:
                        count = n - sum(length * cnt for length, cnt in struct.items())
                    else:
                        count = struct.get(k, 0)
                    
                    if isinstance(m, dict):
                        expected = m.get(k, 0)
                    elif isinstance(m, (list, tuple)):
                        expected = m[k - 1] if len(m) >= k else 0
                    elif callable(m):
                        expected = m(k)
                    else:
                        h2_ok = False
                        break
                    
                    if count != expected:
                        h2_ok = False
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False

    # neg_Q: The number of elements in C is not n! / prod_{k=1}^n (k^{m_k} * m_k!)
    try:
        num = math.factorial(n)
        den = 1
        for k in range(1, n + 1):
            if isinstance(m, dict):
                mk = m.get(k, 0)
            elif isinstance(m, (list, tuple)):
                mk = m[k - 1] if len(m) >= k else 0
            elif callable(m):
                mk = m(k)
            else:
                mk = 0
            den *= (k ** mk) * math.factorial(mk)
        
        expected_size = num // den
        actual_size = len(set(C))
        
        neg_q_ok = actual_size != expected_size
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: The elements of C have a disjoint cycle decomposition consisting of exactly m_k cycles of length k for each 1 <= k <= n",
    "¬Q: The number of elements in C is not n! / ∏_{k=1}^n (k^{m_k} · m_k!)"
]

N_HYP = 2
NEG_Q_INDEX = 2