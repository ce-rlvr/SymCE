import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (n, k).
    """
    try:
        n, k = witness
        n = int(n)
        k = int(k)
    except Exception:
        return [False, False]
    
    # H_1: 1 <= k <= n
    try:
        h1 = bool(1 <= k <= n)
    except Exception:
        h1 = False
        
    # ¬Q: The number of distinct k-cycles in S_n is NOT exactly n! / (k(n-k)!)
    try:
        if 1 <= k <= n:
            # In group theory, a k-cycle is a permutation with exactly one cycle of length k 
            # and all other elements fixed.
            # For k >= 2, the number of such permutations is n! / (k * (n-k)!).
            # For k = 1, a "1-cycle" fixes 1 element and all other elements, meaning it fixes 
            # all elements. Thus, it is the identity permutation. There is exactly 1 identity.
            if k == 1:
                actual_count = 1
            else:
                actual_count = (math.factorial(n) // (math.factorial(k) * math.factorial(n - k))) * math.factorial(k - 1)
                
            formula_count = math.factorial(n) // (k * math.factorial(n - k))
            
            neg_q = bool(actual_count != formula_count)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: 1 <= k <= n",
    "¬Q: The number of distinct k-cycles in S_n is not exactly n! / (k(n-k)!)"
]

N_HYP = 1
NEG_Q_INDEX = 1