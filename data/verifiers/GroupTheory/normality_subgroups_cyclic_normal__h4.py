import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def contains(G, p):
    try:
        return G.contains(p)
    except Exception:
        return p in G.elements

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    for h in H.generators:
        if not contains(G, h):
            return False
    return True

def is_normal_subgroup(H, G):
    if not is_subgroup(H, G):
        return False
    for g in G.generators:
        for h in H.generators:
            if not contains(H, g * h * ~g):
                return False
    return True

def is_cyclic(G):
    try:
        if hasattr(G, 'is_cyclic'):
            res = G.is_cyclic
            if res is not None:
                return bool(res)
    except Exception:
        pass
    
    try:
        order = G.order()
    except Exception:
        order = len(list(G.elements))
        
    for g in G.elements:
        try:
            o = g.order()
        except Exception:
            o = 1
            temp = g
            while not getattr(temp, 'is_Identity', False):
                temp = temp * g
                o += 1
        if o == order:
            return True
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, H) of PermutationGroup objects.
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2_ok = isinstance(N, PermutationGroup) and is_normal_subgroup(N, G)
    except Exception:
        h2_ok = False
        
    # H_3: N is a cyclic group
    try:
        h3_ok = isinstance(N, PermutationGroup) and is_cyclic(N)
    except Exception:
        h3_ok = False
        
    # neg_Q: H is not a normal subgroup of G
    # We require H to be a subgroup of G to form a meaningful counterexample.
    try:
        is_sub = isinstance(H, PermutationGroup) and is_subgroup(H, G)
        is_norm = is_normal_subgroup(H, G)
        neg_q_ok = is_sub and not is_norm
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a cyclic group",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3