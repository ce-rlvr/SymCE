import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def check_normal(H, G):
    if H is None or G is None:
        return False
    try:
        if hasattr(H, 'is_normal'):
            if callable(H.is_normal):
                res = H.is_normal(G)
            else:
                res = H.is_normal
            if res is not None:
                return bool(res)
    except Exception:
        pass
    try:
        if hasattr(G, 'is_normal'):
            if callable(G.is_normal):
                res = G.is_normal(H)
            else:
                res = G.is_normal
            if res is not None:
                return bool(res)
    except Exception:
        pass
    return False

def check_nilpotent(H):
    if H is None:
        return False
    try:
        if hasattr(H, 'is_nilpotent'):
            if callable(H.is_nilpotent):
                res = H.is_nilpotent()
            else:
                res = H.is_nilpotent
            if res is not None:
                return bool(res)
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            M = witness.get('M')
            N = witness.get('N')
            MN = witness.get('MN')
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 4:
                G, M, N, MN = witness
            elif len(witness) == 3:
                G, M, N = witness
                MN = None
            else:
                return [False] * 5
        else:
            return [False] * 5

        if MN is None:
            try:
                MN = M * N
            except Exception:
                pass
        if MN is None:
            try:
                MN = type(G)(*(list(M.generators) + list(N.generators)))
            except Exception:
                pass
        if MN is None:
            try:
                MN = G.subgroup(list(M.generators) + list(N.generators))
            except Exception:
                pass
    except Exception:
        return [False] * 5

    try:
        h1 = check_normal(M, G)
    except Exception:
        h1 = False

    try:
        h2 = check_normal(N, G)
    except Exception:
        h2 = False

    try:
        h3 = check_nilpotent(M)
    except Exception:
        h3 = False

    try:
        h4 = check_nilpotent(N)
    except Exception:
        h4 = False

    try:
        if MN is None:
            neg_q = False
        else:
            mn_normal = check_normal(MN, G)
            mn_nilpotent = check_nilpotent(MN)
            neg_q = not (mn_normal and mn_nilpotent)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: M is a normal subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: M is a nilpotent group",
    "H_4: N is a nilpotent group",
    "¬Q: The product MN is not a normal nilpotent subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4