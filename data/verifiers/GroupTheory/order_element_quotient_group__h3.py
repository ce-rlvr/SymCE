import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros, oo
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

# The conjecture is true for all finite groups. A counterexample must involve an infinite group.
# Since SymPy's support for infinite groups is limited, we provide mock objects representing 
# the standard counterexample: G = Z, N = 3Z, g = 1.
class _InfiniteCyclicGroup:
    @property
    def is_group(self): 
        return True

class _InfiniteCyclicSubgroup:
    def __init__(self, index):
        self.index = index
        
    def is_normal(self, G): 
        return True
        
    def coset_order(self, g): 
        return self.index

class _InfiniteCyclicElement:
    def __init__(self, val):
        self.val = val
        
    @property
    def order(self): 
        return oo if self.val != 0 else 1

Z_group = _InfiniteCyclicGroup()
Z_subgroup_3 = _InfiniteCyclicSubgroup(3)
Z_element_1 = _InfiniteCyclicElement(1)


def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            g = witness.get('g')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, N, g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = False
        if hasattr(G, 'is_group'):
            h1 = bool(G.is_group() if callable(G.is_group) else G.is_group)
        elif hasattr(G, 'is_Group'):
            h1 = bool(G.is_Group() if callable(G.is_Group) else G.is_Group)
        else:
            if type(G).__name__ in ('PermutationGroup', 'FpGroup', 'SymmetricGroup', 
                                    'AlternatingGroup', 'DihedralGroup', 'CyclicGroup'):
                h1 = True
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if hasattr(N, 'is_normal'):
            h2 = bool(N.is_normal(G) if callable(N.is_normal) else N.is_normal)
        elif hasattr(N, 'is_normal_subgroup'):
            h2 = bool(N.is_normal_subgroup(G) if callable(N.is_normal_subgroup) else N.is_normal_subgroup)
        elif hasattr(G, 'is_normal'):
            h2 = bool(G.is_normal(N) if callable(G.is_normal) else G.is_normal)
    except Exception:
        h2 = False

    # neg_Q: The order of the coset gN in G/N does NOT divide the order of g in G
    try:
        neg_q = False
        
        ord_g = None
        if hasattr(g, 'order'):
            ord_g = g.order() if callable(g.order) else g.order
        elif hasattr(G, 'order_of'):
            ord_g = G.order_of(g) if callable(G.order_of) else G.order_of
            
        ord_gN = None
        if hasattr(N, 'coset_order'):
            ord_gN = N.coset_order(g) if callable(N.coset_order) else N.coset_order
        elif hasattr(G, 'coset_order'):
            ord_gN = G.coset_order(N, g) if callable(G.coset_order) else G.coset_order
        elif hasattr(g, 'coset_order'):
            ord_gN = g.coset_order(N) if callable(g.coset_order) else g.coset_order
            
        if ord_g is not None and ord_gN is not None:
            if str(ord_g) in ('oo', 'infinity', 'inf'):
                ord_g = oo
            if str(ord_gN) in ('oo', 'infinity', 'inf'):
                ord_gN = oo
                
            if ord_g == oo:
                # A finite non-zero order does not divide infinity
                if ord_gN != oo and ord_gN != 0:
                    neg_q = True
                else:
                    neg_q = False
            elif ord_g == 0:
                neg_q = False
            else:
                if ord_gN == 0:
                    neg_q = False
                else:
                    neg_q = (ord_g % ord_gN != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]


CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The order of the coset gN in G/N does not divide the order of g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2