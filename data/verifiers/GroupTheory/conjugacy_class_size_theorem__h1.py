import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, x = witness
    except Exception:
        return [False, False]
    
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
        h1_ok = x in elements
    except Exception:
        h1_ok = False

    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        C_G = []
        for g in elements:
            try:
                if g * x == x * g:
                    C_G.append(g)
            except Exception:
                pass
                
        if len(C_G) == 0:
            neg_q_ok = False
        else:
            index = len(elements) / len(C_G)
            
            conj_class = []
            for g in elements:
                inv_g = None
                try:
                    inv_g = ~g
                except Exception:
                    try:
                        inv_g = g**-1
                    except Exception:
                        pass
                
                if inv_g is not None:
                    try:
                        c = g * x * inv_g
                        if c not in conj_class:
                            conj_class.append(c)
                    except Exception:
                        pass
                        
            size_conj = len(conj_class)
            neg_q_ok = abs(size_conj - index) > 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: x is an element of G", "¬Q: The size of the conjugacy class of x is not equal to the index of its centralizer"]
N_HYP = 1
NEG_Q_INDEX = 1