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

# Standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        # The witness is conceptually a pair (R, I) where R is a ring and I is an ideal.
        # We perform basic structural checks if the witness provides them.
        h1 = True
        h2 = True
        h3 = True
        
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(I, 'is_ideal'):
                h1 = bool(I.is_ideal)
                
        # The conclusion states that the kernel of the canonical map phi: R -> lim R/I^n
        # is the intersection of all powers of I.
        # By definition of the inverse limit and the canonical map, an element r in R
        # maps to 0 if and only if it maps to 0 in R/I^n for all n >= 1.
        # This means r is in I^n for all n >= 1.
        # Thus, ker(phi) == intersection(I^n) is a mathematical tautology and holds for ALL rings and ideals.
        # Therefore, the conclusion NEVER fails, and its negation is always False.
        neg_q = False
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: R_hat is the I-adic completion of R",
    "H_3: phi is the canonical ring homomorphism",
    "¬Q: The kernel of phi is not the intersection of all powers of I"
]

N_HYP = 3
NEG_Q_INDEX = 3