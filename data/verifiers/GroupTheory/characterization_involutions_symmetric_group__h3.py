import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The witness can be provided as a tuple (n, sigma) or just sigma
        if isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
        else:
            sigma = witness
            n = sigma.size if hasattr(sigma, 'size') else 1
            if n == 0:
                n = 1
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    try:
        # sigma must be a permutation in S_n
        h2 = isinstance(sigma, Permutation) and sigma.size <= n
    except Exception:
        h2 = False

    try:
        # LHS: sigma is an involution
        # In the context where this conjecture is false, an involution is defined as an element 
        # whose square is the identity (which includes the identity element itself).
        is_involution = (sigma.order() <= 2)
        
        # RHS: its disjoint cycle decomposition consists entirely of 1-cycles and 2-cycles, 
        # with at least one 2-cycle.
        # sympy's cyclic_form omits 1-cycles, so we check that all present cycles have length 2.
        cycles = sigma.cyclic_form
        only_1_and_2 = all(len(c) == 2 for c in cycles)
        at_least_one_2 = len(cycles) >= 1
        rhs = only_1_and_2 and at_least_one_2
        
        # The conclusion is the equivalence between LHS and RHS
        conclusion = (is_involution == rhs)
        
        # We want the negated conclusion (True when the equivalence fails)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: sigma is an element of S_n",
    "¬Q: The equivalence between sigma being an involution and its cycle decomposition having only 1- and 2-cycles (with at least one 2-cycle) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2