import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, k = witness
        else:
            n, k = witness, None
            
        n_int = int(n)
        k_int = int(k)
        h1 = (n_int == n) and (k_int == k) and (1 <= k_int <= n_int)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if n_int > 8:
                neg_q = False
            else:
                count = 0
                for p in SymmetricGroup(n_int).elements:
                    if len(p.cyclic_form) == k_int:
                        count += 1
                
                dp = [[0] * (k_int + 1) for _ in range(n_int + 1)]
                dp[0][0] = 1
                for i in range(1, n_int + 1):
                    for j in range(1, min(i, k_int) + 1):
                        dp[i][j] = (i - 1) * dp[i - 1][j] + dp[i - 1][j - 1]
                expected = dp[n_int][k_int]
                
                neg_q = (count != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n and k are positive integers with 1 <= k <= n",
    "¬Q: The number of elements in S_n that decompose into exactly k disjoint cycles is not the unsigned Stirling number of the first kind"
]

N_HYP = 1
NEG_Q_INDEX = 1