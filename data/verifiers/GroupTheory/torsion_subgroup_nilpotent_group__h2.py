import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, T = witness
        else:
            G = getattr(witness, 'G', None)
            T = getattr(witness, 'T', None)
            if G is None or T is None:
                return [False, False]
    except Exception:
        return [False, False]

    # H_1: G is a nilpotent group
    try:
        h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # neg_Q: T is NOT a normal subgroup of G
    try:
        is_subgroup = True
        if hasattr(T, 'generators'):
            t_gens = T.generators
        else:
            t_gens = list(T)
            if not t_gens:
                is_subgroup = False
            if is_subgroup:
                for a in t_gens:
                    if ~a not in T:
                        is_subgroup = False
                        break
                    for b in t_gens:
                        if a * b not in T:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
        
        if is_subgroup:
            for gen in t_gens:
                if gen not in G:
                    is_subgroup = False
                    break
        
        is_normal = True
        if is_subgroup:
            for g in G.generators:
                for t in t_gens:
                    conj = g * t * (~g)
                    if conj not in T:
                        is_normal = False
                        break
                if not is_normal:
                    break
        
        is_normal_subgroup = is_subgroup and is_normal
        neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: T is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1