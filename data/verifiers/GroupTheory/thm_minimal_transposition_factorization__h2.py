import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture fails because c(sigma) is typically defined as the number of 
    disjoint cycles of length >= 2 (omitting fixed points). The formula n - c(sigma) 
    only gives the minimal number of transpositions if sigma has no fixed points 
    (i.e., sigma is a derangement) or if c(sigma) is redefined to include 1-cycles.
    """
    # H_1: Let sigma be a permutation in the symmetric group S_n
    try:
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    # ¬Q: The minimal number of transpositions required to express sigma as a 
    # product of transpositions is NOT exactly n - c(sigma)
    try:
        if not h1:
            neg_q = False
        else:
            n = witness.size
            
            # c(sigma) as the number of disjoint cycles (excluding 1-cycles/fixed points)
            c_sigma = len(witness.cyclic_form)
            
            # The actual minimal number of transpositions required
            min_trans = sum(len(cycle) - 1 for cycle in witness.cyclic_form)
            
            # The conclusion fails if the actual minimal transpositions != n - c(sigma)
            neg_q = bool(min_trans != n - c_sigma)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in the symmetric group S_n",
    "¬Q: The minimal number of transpositions is not exactly n - c(sigma)"
]

N_HYP = 1
NEG_Q_INDEX = 1