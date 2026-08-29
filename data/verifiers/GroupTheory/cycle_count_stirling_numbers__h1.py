import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group of degree n",
    "¬Q: The number of elements in S_n that decompose into exactly k disjoint cycles is not the unsigned Stirling number of the first kind"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness can be either a degree `n` or a tuple `(n, k)`
        if isinstance(witness, tuple):
            n, k = witness
        else:
            n = witness
            k = None
    except Exception:
        return [False, False]
        
    # H_1: S_n is the symmetric group of degree n
    try:
        h1 = isinstance(n, int) and n >= 1
        if k is not None:
            h1 = h1 and isinstance(k, int) and 1 <= k <= n
        # Prevent memory/time issues for absurdly large witnesses
        if h1 and n > 2000:
            h1 = False
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion FAILS at the witness
    try:
        if not h1:
            neg_q = False
        else:
            max_k = n if k is None else k
            
            # d[m][c] will store the number of derangements of m elements with exactly c cycles.
            # This corresponds to permutations where all cycles have length >= 2 (standard disjoint cycles).
            d = [[0] * (max_k + 1) for _ in range(n + 1)]
            d[0][0] = 1
            for m in range(1, n + 1):
                for c in range(1, max_k + 1):
                    if m >= 2 * c:
                        d[m][c] = (m - 1) * (d[m - 1][c] + d[m - 2][c - 1])
                        
            # s[m][c] will store the unsigned Stirling numbers of the first kind.
            # This corresponds to permutations with exactly c cycles including 1-cycles (fixed points).
            s = [[0] * (max_k + 1) for _ in range(n + 1)]
            s[0][0] = 1
            for m in range(1, n + 1):
                for c in range(1, max_k + 1):
                    s[m][c] = (m - 1) * s[m - 1][c] + s[m - 1][c - 1]
                    
            def check_k_val(k_val):
                # Count permutations in S_n with exactly k_val cycles of length >= 2
                # by summing over the number of fixed points j.
                count = sum(math.comb(n, j) * d[n - j][k_val] for j in range(n + 1))
                expected = s[n][k_val]
                return count == expected
                
            if k is not None:
                # The conclusion fails if the count does not match the Stirling number
                neg_q = not check_k_val(k)
            else:
                # If k is not specified, the conclusion is a universal statement over all k.
                # It fails if it fails for ANY k in 1..n.
                all_match = True
                for k_val in range(1, n + 1):
                    if not check_k_val(k_val):
                        all_match = False
                        break
                neg_q = not all_match
    except Exception:
        neg_q = False
        
    return [h1, neg_q]