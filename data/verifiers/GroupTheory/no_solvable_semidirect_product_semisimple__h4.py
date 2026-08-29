import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(group_obj):
    try:
        if hasattr(group_obj, 'order'):
            ord_val = group_obj.order
            if callable(ord_val):
                return ord_val()
            return ord_val
    except Exception:
        pass
    return 0

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Expected witness: A tuple (G, N, H) where G, N, H are SymPy PermutationGroups.
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial solvable normal subgroups.
    try:
        h1 = False
        if hasattr(G, 'normal_subgroups'):
            h1 = True
            for sub in G.normal_subgroups():
                if get_order(sub) > 1 and getattr(sub, 'is_solvable', False):
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H_2: N is a solvable group
    try:
        h2 = hasattr(N, 'order') and bool(getattr(N, 'is_solvable', False))
    except Exception:
        h2 = False
        
    # H_3: H is a group
    try:
        h3 = hasattr(H, 'order') and hasattr(type(H), 'is_solvable')
    except Exception:
        h3 = False
        
    # neg_Q: N is not the trivial group
    try:
        neg_q = get_order(N) > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: N is a solvable group",
    "H_3: H is a group",
    "¬Q: N is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3