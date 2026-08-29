import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (D, R, f) where:
      - D is the domain group
      - R is the codomain group
      - f is a dictionary or callable representing the homomorphism from D to R
    """
    try:
        D, R, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a reduced abelian group
    try:
        h1 = False
        # Finite abelian groups have no non-trivial divisible subgroups, so they are always reduced.
        if hasattr(R, 'is_abelian') and R.is_abelian and hasattr(R, 'elements'):
            h1 = True
    except Exception:
        h1 = False
        
    # H_2: f: D -> R is a group homomorphism
    try:
        h2 = False
        if hasattr(D, 'elements') and hasattr(R, 'elements'):
            D_elems = list(D.elements)
            R_elems = list(R.elements)
            is_hom = True
            
            if isinstance(f, dict):
                for x in D_elems:
                    if x not in f or f[x] not in R_elems:
                        is_hom = False
                        break
                if is_hom:
                    for x in D_elems:
                        for y in D_elems:
                            if f[x * y] != f[x] * f[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                h2 = is_hom
                
            elif callable(f):
                for x in D_elems:
                    if f(x) not in R_elems:
                        is_hom = False
                        break
                if is_hom:
                    for x in D_elems:
                        for y in D_elems:
                            if f(x * y) != f(x) * f(y):
                                is_hom = False
                                break
                        if not is_hom:
                            break
                h2 = is_hom
    except Exception:
        h2 = False
        
    # ¬Q: f is not the trivial homomorphism
    try:
        neg_q = False
        if hasattr(D, 'elements') and hasattr(R, 'identity'):
            id_R = R.identity
            D_elems = list(D.elements)
            
            if isinstance(f, dict):
                for x in D_elems:
                    if f.get(x) != id_R:
                        neg_q = True
                        break
            elif callable(f):
                for x in D_elems:
                    if f(x) != id_R:
                        neg_q = True
                        break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced abelian group",
    "H_2: f: D -> R is a group homomorphism",
    "¬Q: f is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2