import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G is finitely generated
    try:
        h1_ok = False
        if hasattr(witness, 'is_finitely_generated'):
            val = witness.is_finitely_generated() if callable(witness.is_finitely_generated) else witness.is_finitely_generated
            if val is not None:
                h1_ok = bool(val)
        elif hasattr(witness, 'generators'):
            gens = list(witness.generators)
            h1_ok = True
        elif type(witness).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup']:
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: G is not finitely presented
    try:
        is_fp = None
        if hasattr(witness, 'is_finitely_presented'):
            val = witness.is_finitely_presented() if callable(witness.is_finitely_presented) else witness.is_finitely_presented
            if val is not None:
                is_fp = bool(val)
        
        if is_fp is None:
            if type(witness).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup']:
                is_fp = True
            else:
                # If we cannot determine if it is finitely presented, 
                # we conservatively assume it is, so it fails to be a counterexample.
                is_fp = True 
                
        neg_q_ok = not is_fp
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "¬Q: G is not finitely presented"
]

N_HYP = 1
NEG_Q_INDEX = 1