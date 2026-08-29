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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Localization S^{-1} is a left adjoint functor and therefore commutes 
        # with all colimits, including arbitrary direct sums.
        # Thus, S^{-1}(\bigoplus M_i) is always isomorphic to \bigoplus S^{-1}M_i.
        # Since the conclusion is unconditionally true, its negation is always False.
        neg_q = False
        
        # Best-effort evaluation of hypotheses based on witness type
        if isinstance(witness, str):
            h1 = len(witness.strip()) > 0
            h2 = len(witness.strip()) > 0
        elif isinstance(witness, dict):
            h1 = True
            h2 = True
        elif isinstance(witness, (list, tuple)):
            h1 = len(witness) >= 1
            h2 = len(witness) >= 2
        else:
            h1 = True
            h2 = True
            
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized module S^{-1}(\\bigoplus_{i \\in I} M_i) is NOT isomorphic to \\bigoplus_{i \\in I} (S^{-1}M_i) as S^{-1}R-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2