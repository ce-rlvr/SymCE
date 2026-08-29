import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, x = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    try:
        if isinstance(x, Permutation):
            start = x
            x_elems = [x]
        elif hasattr(x, 'generate'):
            x_elems = list(x.generate())
            start = frozenset(x_elems)
        elif hasattr(x, 'elements'):
            x_elems = list(x.elements)
            start = frozenset(x_elems)
        else:
            x_elems = list(x)
            start = frozenset(x_elems)
            
        g_elements = list(G.generate())
        
        orbit = {start}
        queue = [start]
        
        while queue:
            curr = queue.pop(0)
            for g in g_elements:
                if isinstance(curr, Permutation):
                    nxt = g * curr * g**-1
                else:
                    nxt = frozenset(g * p * g**-1 for p in curr)
                if nxt not in orbit:
                    orbit.add(nxt)
                    queue.append(nxt)
                    
        conj_class_size = len(orbit)
        
        g_order = len(g_elements)
        c_g_order = 0
        for g in g_elements:
            if all(g * p == p * g for p in x_elems):
                c_g_order += 1
                
        if c_g_order == 0:
            neg_q_ok = False
        else:
            index_of_centralizer = g_order / c_g_order
            neg_q_ok = abs(conj_class_size - index_of_centralizer) > 1e-6
            
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "not Q: The size of the conjugacy class of x is not equal to the index of its centralizer"
]
N_HYP = 1
NEG_Q_INDEX = 1