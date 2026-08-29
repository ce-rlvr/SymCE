import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

CONDITION_LABELS = [
    "H_1: H is a group",
    "¬Q: The equivalence (G x H is perfect iff both G and H are perfect) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: H is a group
    try:
        h1 = isinstance(H, sympy.combinatorics.PermutationGroup)
    except Exception:
        h1 = False
        
    # neg_Q: The direct product G x H is perfect if and only if both G and H are perfect.
    try:
        def is_perfect(obj):
            if obj is None:
                return False
            try:
                if isinstance(obj, sympy.combinatorics.PermutationGroup):
                    ds = obj.derived_subgroup() if callable(obj.derived_subgroup) else obj.derived_subgroup
                    ds_order = ds.order() if callable(ds.order) else ds.order
                    obj_order = obj.order() if callable(obj.order) else obj.order
                    return ds_order == obj_order
            except Exception:
                pass
            try:
                if isinstance(obj, (int, sympy.Integer)):
                    n = int(obj)
                    if n <= 0:
                        return False
                    return sum(sympy.ntheory.divisors(n)) == 2 * n
            except Exception:
                pass
            return False

        def direct_product(A, B):
            if isinstance(A, sympy.combinatorics.PermutationGroup) and isinstance(B, sympy.combinatorics.PermutationGroup):
                try:
                    return sympy.combinatorics.DirectProduct(A, B)
                except Exception:
                    pass
            try:
                return A * B
            except Exception:
                return None

        perf_G = is_perfect(G)
        perf_H = is_perfect(H)
        perf_GxH = is_perfect(direct_product(G, H))
        
        q = (perf_GxH == (perf_G and perf_H))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]