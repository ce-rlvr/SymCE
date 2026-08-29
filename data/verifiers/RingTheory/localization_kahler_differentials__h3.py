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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if callable(witness):
            witness = witness()
            
        if isinstance(witness, dict):
            h1 = bool(witness.get('A_is_commutative_ring', False))
            h2 = bool(witness.get('R_is_commutative_A_algebra', False))
            neg_q = not bool(witness.get('isomorphism_holds', True))
        else:
            h1 = bool(getattr(witness, 'A_is_commutative_ring', False))
            h2 = bool(getattr(witness, 'R_is_commutative_A_algebra', False))
            neg_q = not bool(getattr(witness, 'isomorphism_holds', True))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a commutative ring",
    "H_2: R is a commutative A-algebra",
    "¬Q: The isomorphism of S^{-1}R-modules \\Omega_{(S^{-1}R)/A} \\cong S^{-1}\\Omega_{R/A} fails"
]

N_HYP = 2
NEG_Q_INDEX = 2