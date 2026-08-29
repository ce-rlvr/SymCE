import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools

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

def conditions(witness):
    neg_q = False
    try:
        if callable(witness):
            try:
                seq = [witness(i) for i in range(1, 21)]
            except Exception:
                seq = [witness(i) for i in range(20)]
        else:
            try:
                seq = list(itertools.islice(witness, 50))
            except TypeError:
                return [False]
                
        n = len(seq)
        if n > 0:
            inc = [1] * n
            dec = [1] * n
            for i in range(1, n):
                for j in range(i):
                    try:
                        if bool(seq[j] <= seq[i]):
                            if inc[j] + 1 > inc[i]:
                                inc[i] = inc[j] + 1
                    except Exception:
                        pass
                    try:
                        if bool(seq[j] >= seq[i]):
                            if dec[j] + 1 > dec[i]:
                                dec[i] = dec[j] + 1
                    except Exception:
                        pass
            
            max_len = max(max(inc), max(dec))
            
            # Erdős-Szekeres theorem bound:
            # Any sequence of length n from a totally ordered set has a monotone subsequence 
            # of length at least floor(sqrt(n - 1)) + 1.
            # If the longest monotone subsequence is shorter than this bound, the elements 
            # cannot be totally ordered, meaning it is a valid counterexample to the conjecture.
            es_bound = math.floor(math.sqrt(n - 1)) + 1 if n > 0 else 0
            
            if max_len < es_bound:
                neg_q = True
                
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: (x_n) does not have a subsequence that is either non-increasing or non-decreasing"
]
N_HYP = 0
NEG_Q_INDEX = 0