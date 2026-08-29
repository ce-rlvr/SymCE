import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
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
    try:
        G, H, phi, S = witness
    except Exception:
        return [False, False]

    # H_1: S is a subgroup of G
    try:
        h1 = True
        if hasattr(S, 'elements'):
            S_elems = list(S.elements)
        else:
            S_elems = list(S)
            
        if not S_elems:
            h1 = False
        else:
            # Check subset
            for s in S_elems:
                if s not in G:
                    h1 = False
                    break
            
            # Check identity
            if h1:
                has_identity = False
                for e in S_elems:
                    if e * e == e:
                        has_identity = True
                        break
                if not has_identity:
                    h1 = False
            
            # Check closure
            if h1:
                for x in S_elems:
                    for y in S_elems:
                        if x * y not in S_elems:
                            h1 = False
                            break
                    if not h1:
                        break
            
            # Check inverses
            if h1:
                for x in S_elems:
                    if x**-1 not in S_elems:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # ¬Q: The restriction phi|_S is not a group homomorphism or its kernel is not ker(phi) \cap S
    try:
        is_hom = True
        if hasattr(S, 'elements'):
            S_elems = list(S.elements)
        else:
            S_elems = list(S)
            
        for x in S_elems:
            px = phi[x] if isinstance(phi, dict) else phi(x)
            if px not in H:
                is_hom = False
                break
            for y in S_elems:
                py = phi[y] if isinstance(phi, dict) else phi(y)
                pxy = phi[x * y] if isinstance(phi, dict) else phi(x * y)
                if pxy != px * py:
                    is_hom = False
                    break
            if not is_hom:
                break
        neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subgroup of G",
    "¬Q: The restriction phi|_S is not a group homomorphism or its kernel is not ker(phi) intersection S"
]

N_HYP = 1
NEG_Q_INDEX = 1