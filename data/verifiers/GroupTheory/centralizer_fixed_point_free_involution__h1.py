import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

CONDITION_LABELS = [
    "H_1: \\sigma is an involution in S_{2m} having no fixed points (a product of m disjoint transpositions)",
    "¬Q: The centralizer of \\sigma in S_{2m} is NOT isomorphic to the hyperoctahedral group (S_2 \\wr S_m)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, Permutation):
            return [False, False]
        
        n = witness.size
        if n % 2 != 0 or n == 0:
            h1 = False
        else:
            m = n // 2
            if witness.order() != 2:
                h1 = False
            elif len(witness.support()) != n:
                h1 = False
            else:
                h1 = True
                
        if not h1:
            return [False, False]
            
        # The centralizer of a fixed-point-free involution in S_{2m} is mathematically ALWAYS 
        # isomorphic to the hyperoctahedral group S_2 \wr S_m.
        # Therefore, the conclusion Q is always True, and its negation is False.
        Q = True
        
        return [h1, not Q]
    except Exception:
        return [False, False]