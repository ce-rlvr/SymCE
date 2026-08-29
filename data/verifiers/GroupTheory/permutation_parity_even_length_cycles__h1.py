import sympy
from sympy.combinatorics import Permutation
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple: (sigma, k)
    """
    try:
        sigma, k = witness
    except Exception:
        return [False, False]
        
    # H_1: k is the number of cycles of even length in the disjoint cycle decomposition of σ
    try:
        cycles = sigma.cyclic_form
        k_actual = sum(1 for c in cycles if len(c) % 2 == 0)
        h1_ok = (k == k_actual)
    except Exception:
        h1_ok = False
        
    # neg_Q: The conclusion is "σ is an even permutation if and only if k is an even integer".
    # We want the negation of this conclusion (i.e., the biconditional fails).
    try:
        is_even_perm = bool(sigma.is_even)
        is_k_even = bool(k % 2 == 0)
        neg_q_ok = (is_even_perm != is_k_even)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is the number of cycles of even length in the disjoint cycle decomposition of σ",
    "¬Q: (σ is an even permutation) is not equivalent to (k is an even integer)"
]

N_HYP = 1
NEG_Q_INDEX = 1