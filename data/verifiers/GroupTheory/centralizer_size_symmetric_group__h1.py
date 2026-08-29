import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
    try:
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    try:
        # H2 is a definitional statement for m_k, so it holds for any valid permutation
        h2 = isinstance(witness, Permutation)
    except Exception:
        h2 = False

    try:
        if not isinstance(witness, Permutation):
            neg_q = False
        else:
            # The actual centralizer size in S_n accounts for all elements, including fixed points (1-cycles).
            full_lens = [len(c) for c in witness.full_cyclic_form]
            actual_size = 1
            for k in set(full_lens):
                count = full_lens.count(k)
                actual_size *= (k ** count) * math.factorial(count)
            
            # The formula in the conclusion uses the standard disjoint cycle decomposition,
            # which conventionally omits 1-cycles (fixed points).
            disjoint_lens = [len(c) for c in witness.cyclic_form]
            formula_size = 1
            for k in set(disjoint_lens):
                count = disjoint_lens.count(k)
                formula_size *= (k ** count) * math.factorial(count)
            
            # The conclusion fails if the formula size does not match the actual centralizer size.
            # This happens when the permutation has 2 or more fixed points.
            neg_q = actual_size != formula_size
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in S_n",
    "H_2: For each k >= 1, m_k is the number of cycles of length k in the disjoint cycle decomposition of sigma",
    "¬Q: The size of the centralizer of sigma in S_n is not prod_{k=1}^n k^{m_k} (m_k!)"
]

N_HYP = 2
NEG_Q_INDEX = 2