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

from sympy.polys.domains.ring import Ring
from sympy.polys.domains.field import Field
from sympy.polys.agca.ideals import Ideal

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness is expected to be a tuple (R, I) where R is a SymPy Ring/Field
    and I is an Ideal or a list of generators in R.
    """
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a ring
    try:
        h1_ok = isinstance(R, (Ring, Field))
    except Exception:
        h1_ok = False
        
    # H_2: I is an ideal of R
    try:
        if isinstance(I, Ideal):
            h2_ok = (I.ring == R)
        else:
            h2_ok = isinstance(I, (list, tuple, set))
            if h2_ok:
                for gen in I:
                    if gen not in R:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False
        
    # ¬Q: The kernel of phi is NOT the intersection of all powers of I.
    # By definition of the inverse limit \varprojlim R/I^n, the kernel of the 
    # canonical homomorphism \phi: R -> \varprojlim R/I^n is exactly the 
    # intersection of the kernels of the projections R -> R/I^n, which are I^n.
    # Thus, \ker \phi = \bigcap_{n=1}^\infty I^n is a set-theoretic tautology 
    # that holds for any ring and any ideal. It can never fail.
    try:
        neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "¬Q: The kernel of phi is not the intersection of all powers of I"
]

N_HYP = 2
NEG_Q_INDEX = 2