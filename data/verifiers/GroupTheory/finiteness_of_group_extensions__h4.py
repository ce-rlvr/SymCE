import sympy
from sympy.combinatorics import (
    PermutationGroup, AlternatingGroup, SymmetricGroup, 
    CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        else:
            G = witness.G
            N = witness.N
    except Exception:
        return [False, False, False, False]

    def is_group(obj):
        if hasattr(obj, 'is_group'):
            return bool(obj.is_group() if callable(obj.is_group) else obj.is_group)
        class_name = type(obj).__name__
        if 'Group' in class_name or 'group' in class_name.lower():
            return True
        return False

    def is_finite(obj):
        if hasattr(obj, 'is_finite'):
            return bool(obj.is_finite() if callable(obj.is_finite) else obj.is_finite)
        if hasattr(obj, 'order'):
            order = obj.order() if callable(obj.order) else obj.order
            return order < math.inf and order != sympy.oo
        class_name = type(obj).__name__
        if class_name in ['PermutationGroup', 'SymmetricGroup', 'AlternatingGroup', 'CyclicGroup', 'DihedralGroup']:
            return True
        if class_name == 'FreeGroup':
            return len(obj.generators) == 0
        return False

    def is_normal_subgroup(N, G):
        if hasattr(G, 'is_normal'):
            if callable(G.is_normal):
                try: 
                    res = G.is_normal(N)
                    if res is not None: return bool(res)
                except Exception: pass
                try:
                    res = G.is_normal()
                    if res is not None: return bool(res)
                except Exception: pass
            else:
                return bool(G.is_normal)
                
        if hasattr(N, 'is_normal_in'):
            if callable(N.is_normal_in):
                try: 
                    res = N.is_normal_in(G)
                    if res is not None: return bool(res)
                except Exception: pass
            else:
                return bool(N.is_normal_in)
                
        if hasattr(N, 'is_normal'):
            if callable(N.is_normal):
                try: 
                    res = N.is_normal(G)
                    if res is not None: return bool(res)
                except Exception: pass
                try:
                    res = N.is_normal()
                    if res is not None: return bool(res)
                except Exception: pass
            else:
                return bool(N.is_normal)
                
        if hasattr(G, 'is_normal_subgroup'):
            if callable(G.is_normal_subgroup):
                try: 
                    res = G.is_normal_subgroup(N)
                    if res is not None: return bool(res)
                except Exception: pass
            else:
                return bool(G.is_normal_subgroup)
                
        return False

    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    try:
        h2 = is_normal_subgroup(N, G)
    except Exception:
        h2 = False

    try:
        h3 = is_finite(N)
    except Exception:
        h3 = False

    try:
        neg_q = not is_finite(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]