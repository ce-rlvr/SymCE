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
    try:
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    try:
        # P: sigma is an involution (i.e., its own inverse, sigma^2 = id)
        is_involution = (witness == ~witness)
        
        # Q: disjoint cycle decomposition consists entirely of 1-cycles and 2-cycles, 
        # with at least one 2-cycle.
        # SymPy's cyclic_form omits 1-cycles, so we check that all present cycles 
        # have length 2, and there is at least one such cycle.
        cycles = witness.cyclic_form
        only_1_and_2_cycles = all(len(c) == 2 for c in cycles)
        at_least_one_2_cycle = len(cycles) >= 1
        
        q = only_1_and_2_cycles and at_least_one_2_cycle
        
        # The conclusion is P <-> Q. It fails if P != q.
        neg_q = bool(is_involution != q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation",
    "¬Q: sigma being an involution is not equivalent to its cycle decomposition having only 1- and 2-cycles with at least one 2-cycle"
]

N_HYP = 1
NEG_Q_INDEX = 1