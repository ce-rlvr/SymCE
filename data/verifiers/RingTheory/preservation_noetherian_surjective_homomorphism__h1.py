import sympy
from sympy import *
import sympy.combinatorics
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

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, dict):
            if 'is_surjective_homomorphism' in witness:
                H1 = bool(witness['is_surjective_homomorphism'])
            if 'R_is_noetherian' in witness:
                H2 = bool(witness['R_is_noetherian'])
            if 'S_is_noetherian' in witness:
                neg_Q = not bool(witness['S_is_noetherian'])
            
            if 'is_surjective_homomorphism' in witness or 'R_is_noetherian' in witness or 'S_is_noetherian' in witness:
                return [H1, H2, neg_Q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, f = witness
            
            if hasattr(f, 'is_surjective_homomorphism'):
                H1 = bool(f.is_surjective_homomorphism)
            elif hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
                H1 = bool(f.is_surjective) and bool(f.is_homomorphism)
            elif isinstance(f, dict) and 'is_surjective_homomorphism' in f:
                H1 = bool(f['is_surjective_homomorphism'])
                
            if hasattr(R, 'is_noetherian'):
                H2 = bool(R.is_noetherian)
            elif isinstance(R, dict) and 'is_noetherian' in R:
                H2 = bool(R['is_noetherian'])
                
            if hasattr(S, 'is_noetherian'):
                neg_Q = not bool(S.is_noetherian)
            elif isinstance(S, dict) and 'is_noetherian' in S:
                neg_Q = not bool(S['is_noetherian'])
                
            return [H1, H2, neg_Q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_surjective_homomorphism'):
            H1 = bool(witness.is_surjective_homomorphism)
        if hasattr(witness, 'R_is_noetherian'):
            H2 = bool(witness.R_is_noetherian)
        if hasattr(witness, 'S_is_noetherian'):
            neg_Q = not bool(witness.S_is_noetherian)
    except Exception:
        pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: f: R -> S is a surjective ring homomorphism",
    "H_2: R is a Noetherian ring",
    "¬Q: S is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2