import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (F, k) where F is a group and k is an index.
    """
    try:
        F, k = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: F is a finitely generated free group
        h1 = type(F).__name__ == 'FreeGroup' and hasattr(F, 'generators') and len(F.generators) < float('inf')
    except Exception:
        h1 = False
        
    try:
        # ¬Q: There are infinitely many distinct subgroups of F that have index k.
        # A finitely generated free group has infinitely many subgroups of index k 
        # if and only if k is infinite and the rank of the free group is at least 2.
        if k == sympy.oo or k == math.inf or k == float('inf'):
            neg_q = len(F.generators) >= 2
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "¬Q: There are infinitely many distinct subgroups of F that have index k"
]

N_HYP = 1
NEG_Q_INDEX = 1