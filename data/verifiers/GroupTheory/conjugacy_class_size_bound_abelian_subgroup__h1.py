import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, A, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: A is an abelian subgroup of G
    try:
        if hasattr(A, 'is_subgroup'):
            h1_sub = A.is_subgroup(G)
        else:
            g_elems = list(G.generate_dimino()) if hasattr(G, 'generate_dimino') else list(G.elements)
            a_elems = list(A.generate_dimino()) if hasattr(A, 'generate_dimino') else list(A.elements)
            h1_sub = all(a in g_elems for a in a_elems)
            
        if hasattr(A, 'is_abelian'):
            h1_ab = A.is_abelian
            if callable(h1_ab):
                h1_ab = h1_ab()
        else:
            a_elems = list(A.generate_dimino()) if hasattr(A, 'generate_dimino') else list(A.elements)
            h1_ab = all(a * b == b * a for a in a_elems for b in a_elems)
            
        h1 = bool(h1_sub and h1_ab)
    except Exception:
        h1 = False
        
    # H_2: x is an element of A
    try:
        if hasattr(A, 'contains'):
            h2 = A.contains(x)
        else:
            a_elems = list(A.generate_dimino()) if hasattr(A, 'generate_dimino') else list(A.elements)
            h2 = x in a_elems
        h2 = bool(h2)
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x in G is greater than the index of A in G
    try:
        elements = list(G.generate_dimino()) if hasattr(G, 'generate_dimino') else list(G.elements)
            
        conj_class = set()
        for g in elements:
            inv_g = ~g if hasattr(g, '__invert__') else g**-1
            elem = g * x * inv_g
            try:
                hash(elem)
                conj_class.add(elem)
            except TypeError:
                conj_class.add(str(elem))
                
        conj_size = len(conj_class)
        
        g_order = G.order() if callable(getattr(G, 'order', None)) else getattr(G, 'order', len(elements))
        
        if hasattr(A, 'order'):
            a_order = A.order() if callable(A.order) else A.order
        else:
            a_elems = list(A.generate_dimino()) if hasattr(A, 'generate_dimino') else list(A.elements)
            a_order = len(a_elems)
                
        index = g_order / a_order
        
        neg_q = bool(conj_size > index)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian subgroup of G",
    "H_2: x is an element of A",
    "¬Q: The size of the conjugacy class of x in G is greater than the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2