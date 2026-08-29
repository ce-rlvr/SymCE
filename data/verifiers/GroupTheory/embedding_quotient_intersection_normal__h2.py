import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for witness expressions
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
    The witness should be a tuple (G, N1, N2) where G is a group and N1, N2 are subgroups.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        G, N1, N2 = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a group, and N1, N2 are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N1, PermutationGroup) and 
              isinstance(N2, PermutationGroup) and 
              N1.is_subgroup(G) and 
              N2.is_subgroup(G))
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails at the witness.
    # The conclusion states that G/(N1 \cap N2) is isomorphic to a subgroup of (G/N1) x (G/N2).
    # This requires G/N1 and G/N2 to be well-defined quotient groups, which means N1 and N2 must be normal in G.
    # If both are normal, the theorem holds (conclusion is true, so neg_Q is false).
    # If at least one is not normal, the quotient group structure is undefined, so the conclusion fails (neg_Q is true).
    try:
        if not h1:
            neg_q = False
        else:
            def is_normal(grp, subgrp):
                if not subgrp.is_subgroup(grp):
                    return False
                for g in grp.generators:
                    for h in subgrp.generators:
                        if (g * h * ~g) not in subgrp:
                            return False
                        if (~g * h * g) not in subgrp:
                            return False
                return True
            
            normal1 = is_normal(G, N1)
            normal2 = is_normal(G, N2)
            
            if normal1 and normal2:
                neg_q = False
            else:
                neg_q = True
                
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N_1, N_2 are subgroups of G",
    "¬Q: G/(N_1 \\cap N_2) is not isomorphic to a subgroup of (G/N_1) \\times (G/N_2)"
]

N_HYP = 1
NEG_Q_INDEX = 1