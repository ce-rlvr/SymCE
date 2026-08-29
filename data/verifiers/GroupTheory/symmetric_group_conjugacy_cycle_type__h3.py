import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (n, G, sigma, tau)
    """
    try:
        n, G, sigma, tau = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False
        
    # H_2: G is the symmetric group S_n
    try:
        h2_ok = (G == SymmetricGroup(n))
    except Exception:
        h2_ok = False
        
    # ¬Q: It is NOT the case that (sigma and tau are conjugate in G iff they have the same cycle type)
    try:
        # Check if they have the same cycle type
        same_cycle_type = (sigma.cycle_structure == tau.cycle_structure)
        
        # Check if they are conjugate in G
        conjugate_in_G = False
        for g in G.elements:
            if g * sigma * g**-1 == tau:
                conjugate_in_G = True
                break
                
        # The conclusion is (conjugate_in_G == same_cycle_type)
        # We want the negation of the conclusion
        neg_q_ok = (conjugate_in_G != same_cycle_type)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the symmetric group S_n",
    "¬Q: Conjugacy of sigma and tau in G is not equivalent to them having the same cycle type"
]

N_HYP = 2
NEG_Q_INDEX = 2