import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return set(obj.elements)
    elif hasattr(obj, 'generate'):
        return set(obj.generate())
    elif isinstance(obj, (set, list, tuple)):
        return set(obj)
    else:
        raise ValueError("Cannot get elements")

def conditions(witness) -> list[bool]:
    # Unpack witness
    G = None
    H = None
    N = None
    HN = None
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            N = witness['N']
            HN = witness.get('HN', None)
        else:
            G = witness[0]
            H = witness[1]
            N = witness[2]
            if len(witness) > 3:
                HN = witness[3]
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        G_elems = get_elements(G)
        H1 = len(G_elems) > 0
    except Exception:
        H1 = False

    # H_2: H is a subgroup of G
    try:
        H_elems = get_elements(H)
        H2 = H_elems.issubset(G_elems) and len(H_elems) > 0
        if H2:
            if hasattr(H, 'is_subgroup'):
                H2 = H.is_subgroup(G)
            else:
                is_closed = True
                for h1 in H_elems:
                    for h2 in H_elems:
                        if h1 * h2 not in H_elems:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                H2 = is_closed
    except Exception:
        H2 = False

    # H_3: HN is the set containing all products hn where h in H and n in N
    try:
        N_elems = get_elements(N)
        H3 = N_elems.issubset(G_elems) and len(N_elems) > 0
        
        HN_computed = {h * n for h in H_elems for n in N_elems}
        
        if HN is not None:
            HN_provided = get_elements(HN)
            H3 = H3 and (HN_provided == HN_computed)
    except Exception:
        H3 = False

    # ¬Q: The index of N in HN does NOT divide the order of H
    try:
        len_HN = len(HN_computed)
        len_N = len(N_elems)
        len_H = len(H_elems)
        
        if len_N == 0:
            neg_Q = False
        else:
            # If the ratio is not an integer, it does not divide |H|
            if len_HN % len_N != 0:
                neg_Q = True
            else:
                index = len_HN // len_N
                if index == 0:
                    neg_Q = True
                else:
                    neg_Q = (len_H % index != 0)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: HN is the set containing all products hn where h in H and n in N",
    "¬Q: The index of N in HN does not divide the order of H"
]

N_HYP = 3
NEG_Q_INDEX = 3