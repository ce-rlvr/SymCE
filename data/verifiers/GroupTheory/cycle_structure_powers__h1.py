import math
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        if isinstance(witness, tuple):
            if len(witness) == 3:
                sigma, k, n = witness
            elif len(witness) == 2:
                sigma, k = witness
                n = sigma.size
            else:
                sigma, k, n = None, None, None
        else:
            sigma, k, n = None, None, None
    except Exception:
        sigma, k, n = None, None, None

    # H_1: k is a positive integer
    try:
        h1 = isinstance(k, int) and k > 0
    except Exception:
        h1 = False

    # ¬Q: sigma^k is NOT a product of gcd(n, k) disjoint cycles, each of length n / gcd(n, k)
    try:
        if not isinstance(sigma, Permutation):
            neg_q = False
        elif not isinstance(n, int) or n <= 0:
            neg_q = False
        elif not (isinstance(k, int) and k > 0):
            neg_q = False
        else:
            expected_num_cycles = math.gcd(n, k)
            expected_length = n // expected_num_cycles
            
            p_k = sigma ** k
            cycles = p_k.cyclic_form
            moved = set(e for c in cycles for e in c)
            
            if any(e >= n for e in moved):
                q_holds = False
            else:
                num_cycles = len(cycles) + (n - len(moved))
                lengths = [len(c) for c in cycles] + [1] * (n - len(moved))
                
                q_holds = (num_cycles == expected_num_cycles) and all(l == expected_length for l in lengths)
            
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: sigma^k is not a product of gcd(n, k) disjoint cycles, each of length n / gcd(n, k)"
]

N_HYP = 1
NEG_Q_INDEX = 1