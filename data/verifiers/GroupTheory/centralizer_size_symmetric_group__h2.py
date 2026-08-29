import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple (n, sigma)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        n, sigma = witness
    except Exception:
        return [False, False, False]

    # H_1: S_n is the symmetric group on n letters
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H_2: For each k >= 1, m_k is the number of cycles of length k in the disjoint cycle decomposition of sigma
    try:
        h2 = isinstance(sigma, Permutation)
    except Exception:
        h2 = False

    # neg_Q: The size of the centralizer of sigma in S_n is NOT prod_{k=1}^n k^{m_k} (m_k!)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if n > 8:
                # Prevent timeout for excessively large n
                neg_q = False
            else:
                Sn = SymmetricGroup(n)
                actual_size = 0
                
                # Calculate the actual size of the centralizer of sigma in S_n
                for tau in Sn.generate():
                    if tau * sigma == sigma * tau:
                        actual_size += 1

                # Calculate the formula prod_{k=1}^n k^{m_k} (m_k!)
                cycles = sigma.full_cyclic_form
                formula_val = 1
                for k in range(1, n + 1):
                    m_k = sum(1 for c in cycles if len(c) == k)
                    formula_val *= (k ** m_k) * math.factorial(m_k)

                neg_q = actual_size != formula_val
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: For each k >= 1, m_k is the number of cycles of length k in the disjoint cycle decomposition of sigma",
    "¬Q: The size of the centralizer of sigma in S_n is not prod_{k=1}^n k^{m_k} (m_k!)"
]

N_HYP = 2
NEG_Q_INDEX = 2