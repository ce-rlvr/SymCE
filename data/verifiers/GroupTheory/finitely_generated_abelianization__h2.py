import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
    H1 = False
    try:
        class_name = type(witness).__name__
        if isinstance(witness, PermutationGroup) or class_name == 'FpGroup':
            H1 = True
        elif class_name == 'FreeGroup':
            H1 = len(witness.generators) < float('inf')
        elif hasattr(witness, 'generators'):
            H1 = len(list(witness.generators)) < float('inf')
    except Exception:
        H1 = False

    neg_Q = False
    try:
        Q = False
        if hasattr(witness, 'abelian_invariants'):
            try:
                invs = witness.abelian_invariants()
                if isinstance(invs, list):
                    Q = True
            except Exception:
                pass
        
        # Mathematically, the abelianization G/G' of a finitely generated group G 
        # is always a finitely generated abelian group.
        if not Q:
            if H1:
                Q = True
                
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: The quotient group G/G' is not a finitely generated abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1