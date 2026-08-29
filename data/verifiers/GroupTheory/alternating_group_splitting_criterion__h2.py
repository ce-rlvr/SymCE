import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup

# Top-level setup
# (No specific named objects are required for this witness namespace)

def conditions(witness) -> list[bool]:
    try:
        n, x = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False
        
    try:
        # Check if x is a valid permutation in S_n
        # In sympy, a permutation's size is max(moved) + 1. 
        # For S_n (acting on 0 to n-1), the size must be <= n.
        h2 = isinstance(x, Permutation) and x.size <= n
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # Evaluate Q: The centralizer of x in S_n is contained in A_n.
            # This holds if and only if x commutes with no odd permutation.
            # A permutation commutes with no odd permutation iff all its cycles 
            # (including 1-cycles) have distinct odd lengths.
            cycle_counts = x.cycle_structure.copy()
            sum_len = sum(k * v for k, v in cycle_counts.items())
            ones = n - sum_len
            if ones > 0:
                cycle_counts[1] = cycle_counts.get(1, 0) + ones
                
            Q = True
            for k, v in cycle_counts.items():
                if k % 2 == 0 or v > 1:
                    Q = False
                    break
                    
            # Evaluate P: K splits into exactly two distinct conjugacy classes in A_n.
            # K is the conjugacy class of x in S_n.
            # K splits into exactly two conjugacy classes in A_n iff K is a subset of A_n 
            # (i.e., x is an even permutation) AND the centralizer condition (Q) holds.
            is_even = x.is_even
            P = is_even and Q
            
            # The conclusion is P <-> Q. We want the negation of the conclusion.
            neg_q = not (P == Q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: K is the conjugacy class of x in the symmetric group S_n",
    "¬Q: It is NOT the case that (K splits into exactly two distinct conjugacy classes in A_n iff the centralizer of x in S_n is contained in A_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2