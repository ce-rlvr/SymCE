import math
import itertools
import functools
import sympy
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
    try:
        # The witness is expected to be a permutation group.
        # The dropped hypothesis was that the group is the symmetric group S_n.
        if not hasattr(witness, 'degree') or not hasattr(witness, 'generate'):
            return [False, False]
        
        n = witness.degree
        
        # H_1: Let D_n denote the number of permutations in the group that have no fixed points.
        # We compute D_n for the witness group.
        D_n = 0
        for p in witness.generate():
            # A permutation is a derangement if it has no fixed points in 0, ..., n-1
            if all(p(i) != i for i in range(n)):
                D_n += 1
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        # Conclusion: D_n = n! \sum_{k=0}^n \frac{(-1)^k}{k!}
        # We compute the exact integer value of the formula to avoid float precision issues.
        formula = 0
        for k in range(n + 1):
            term = math.factorial(n) // math.factorial(k)
            if k % 2 == 1:
                formula -= term
            else:
                formula += term
                
        # The negated conclusion is True if the computed D_n does not match the formula.
        neg_q = (D_n != formula)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let D_n denote the number of permutations in S_n that have no fixed points",
    "¬Q: D_n != n! \\sum_{k=0}^n \\frac{(-1)^k}{k!}"
]

N_HYP = 1
NEG_Q_INDEX = 1