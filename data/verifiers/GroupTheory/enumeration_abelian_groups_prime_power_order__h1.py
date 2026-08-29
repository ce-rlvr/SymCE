import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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

def partition_function(n):
    n = int(n)
    if n < 0: 
        return 0
    if n == 0: 
        return 1
    partitions = [0] * (n + 1)
    partitions[0] = 1
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            partitions[j] += partitions[j - i]
    return partitions[n]

def num_abelian_groups(k):
    k = int(k)
    if k < 1:
        raise ValueError("Order must be a positive integer")
    factors = factorint(k)
    ans = 1
    for base, exp in factors.items():
        ans *= partition_function(exp)
    return ans

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            n = witness['n']
        else:
            p, n = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False
        
    try:
        k = p**n
        actual_classes = num_abelian_groups(k)
        expected_classes = partition_function(n)
        neg_q = bool(actual_classes != expected_classes)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The number of isomorphism classes of abelian groups of order p^n is not equal to P(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1