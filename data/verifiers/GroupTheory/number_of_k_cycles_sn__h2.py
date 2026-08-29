import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        n, k = witness
    except Exception:
        return [False, False]
        
    # H_1: n and k are integers
    try:
        h1 = (int(n) == n) and (int(k) == k)
    except Exception:
        h1 = False
        
    # ¬Q: The number of distinct k-cycles in S_n is NOT exactly n! / (k(n-k)!)
    try:
        if not h1:
            neg_q = False
        else:
            n_int = int(n)
            k_int = int(k)
            
            # Calculate the actual number of distinct k-cycles in S_n
            if n_int < 0:
                actual = 0
            elif k_int == 1:
                # A 1-cycle is just the identity permutation. There is exactly 1 in S_n (for n >= 1).
                actual = 1 if n_int >= 1 else 0
            elif 2 <= k_int <= n_int:
                # Standard combinatorial formula for k-cycles when 2 <= k <= n
                actual = math.comb(n_int, k_int) * math.factorial(k_int - 1)
            else:
                actual = 0
                
            # Calculate the value given by the formula n! / (k(n-k)!)
            try:
                num = math.factorial(n_int)
                den = k_int * math.factorial(n_int - k_int)
                if den == 0:
                    formula = None
                else:
                    formula = num / den
            except Exception:
                # If factorials are undefined (e.g., negative inputs), the formula is undefined
                formula = None
                
            # The conclusion fails if the actual count does not match the formula's result
            neg_q = (actual != formula)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n and k are integers",
    "¬Q: The number of distinct k-cycles in S_n is not exactly n! / (k(n-k)!)"
]

N_HYP = 1
NEG_Q_INDEX = 1