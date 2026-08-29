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

def is_in_G(G, x):
    try:
        if hasattr(G, '__contains__'):
            return bool(x in G)
        if hasattr(G, 'contains'):
            return bool(G.contains(x))
        elements = G.elements if hasattr(G, 'elements') else G
        return bool(x in elements)
    except Exception:
        return False

def in_center(G, x):
    try:
        if hasattr(G, 'center'):
            C = G.center()
            if hasattr(C, '__contains__'):
                return bool(x in C)
            if hasattr(C, 'contains'):
                return bool(C.contains(x))
        
        elements = G.elements if hasattr(G, 'elements') else G
        for g in elements:
            if g * x != x * g:
                return False
        return True
    except Exception:
        return False

def conjugacy_class_size(G, x):
    try:
        if hasattr(G, 'order') and hasattr(G, 'centralizer'):
            try:
                C = G.centralizer(x)
                return G.order() // C.order()
            except Exception:
                try:
                    C = G.centralizer([x])
                    return G.order() // C.order()
                except Exception:
                    pass
                    
        elements = G.elements if hasattr(G, 'elements') else G
        conj_class = []
        for g in elements:
            try:
                inv_g = g**-1
            except Exception:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g.inv()
            conj_elem = g * x * inv_g
            if conj_elem not in conj_class:
                conj_class.append(conj_elem)
        return len(conj_class)
    except Exception:
        return -1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G, x = witness.G, witness.x
    except Exception:
        return [False, False]
        
    try:
        h1 = is_in_G(G, x)
    except Exception:
        h1 = False
        
    try:
        center_check = in_center(G, x)
        cc_size = conjugacy_class_size(G, x)
        if cc_size == -1:
            neg_q = False
        else:
            q = (center_check == (cc_size == 1))
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: x in Z(G) is not equivalent to |Cl(x)| == 1"
]

N_HYP = 1
NEG_Q_INDEX = 1