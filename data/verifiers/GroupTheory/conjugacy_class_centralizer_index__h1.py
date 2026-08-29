import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        if len(witness) == 3:
            G, x, C = witness
        elif len(witness) == 2:
            G, x = witness
            C = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: x is an element of G
    try:
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        elif hasattr(G, 'generate'):
            G_elements = list(G.generate())
        else:
            G_elements = list(G)
        h1 = x in G_elements
    except Exception:
        h1 = False
        
    # H_2: C_G(x) is the centralizer of x in G
    try:
        expected_C = []
        for g in G_elements:
            if g * x == x * g:
                expected_C.append(g)
        
        if C is None:
            C_elements = expected_C
            h2 = True
        else:
            if hasattr(C, 'elements'):
                C_elements = list(C.elements)
            elif hasattr(C, 'generate'):
                C_elements = list(C.generate())
            else:
                C_elements = list(C)
                
            if len(C_elements) != len(expected_C):
                h2 = False
            else:
                h2 = all(c in expected_C for c in C_elements) and all(c in C_elements for c in expected_C)
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G
    try:
        conj_class = []
        for g in G_elements:
            try:
                g_inv = g.inv()
            except AttributeError:
                try:
                    g_inv = ~g
                except TypeError:
                    g_inv = g**-1
            
            conj = g * x * g_inv
            if conj not in conj_class:
                conj_class.append(conj)
                
        size_conj = len(conj_class)
        if len(C_elements) == 0:
            neg_q = False
        else:
            index = len(G_elements) / len(C_elements)
            neg_q = abs(size_conj - index) > 1e-9
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: C_G(x) is the centralizer of x in G",
    "¬Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2