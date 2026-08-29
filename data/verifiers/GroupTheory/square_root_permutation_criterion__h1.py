import sympy
from sympy.combinatorics import Permutation, SymmetricGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    # H_1: Let \sigma \in S_n be a permutation
    try:
        h1_ok = isinstance(witness, Permutation)
    except Exception:
        h1_ok = False

    # neg_Q: \sigma has a square root in S_n if and only if for every even integer k, 
    # the number of cycles of length k in the disjoint cycle decomposition of \sigma is even
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            sigma = witness
            n = sigma.size
            
            # Check if sigma has a square root in S_n
            has_square_root = False
            if n > 0:
                # Generate all permutations in S_n to check for a square root
                # Note: For small n, this is fast enough.
                for p in itertools.permutations(range(n)):
                    tau = Permutation(p)
                    if (tau * tau) == sigma:
                        has_square_root = True
                        break
            else:
                has_square_root = True  # S_0 has 1 element, which is its own square root
            
            # Check the condition: for every even integer k, the number of cycles of length k is even
            # Get cycle lengths including 1-cycles (fixed points)
            cycle_lengths = [len(c) for c in sigma.full_cyclic_form]
            
            # Count frequencies of each cycle length
            length_counts = {}
            for length in cycle_lengths:
                length_counts[length] = length_counts.get(length, 0) + 1
                
            condition_holds = True
            for k, count in length_counts.items():
                if k % 2 == 0 and count % 2 != 0:
                    condition_holds = False
                    break
            
            # The conclusion is the equivalence of the two statements
            conclusion = (has_square_root == condition_holds)
            
            # We want the negation of the conclusion
            neg_q_ok = not conclusion
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: sigma is a permutation",
    "¬Q: It is NOT the case that (sigma has a square root in S_n iff for every even integer k, the number of cycles of length k is even)"
]

N_HYP = 1
NEG_Q_INDEX = 1