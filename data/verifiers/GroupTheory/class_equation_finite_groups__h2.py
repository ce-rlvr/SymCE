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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, X = witness
            try:
                elements = list(G.elements)
                C = []
                for x in X:
                    actual_c = set(g for g in elements if g * x == x * g)
                    C.append(actual_c)
            except Exception:
                C = []
        elif len(witness) == 3:
            G, X, C = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        H1 = hasattr(G, 'elements') and len(list(G.elements)) > 0
    except Exception:
        H1 = False

    # H2: {x_1, ..., x_k} is a complete set of representatives of the distinct conjugacy classes of G of size greater than 1
    try:
        elements = list(G.elements)
        classes = []
        seen = set()
        for g in elements:
            if g not in seen:
                c = set()
                for h in elements:
                    c.add(h * g * ~h)
                classes.append(c)
                seen.update(c)
        
        classes_gt_1 = [c for c in classes if len(c) > 1]
        
        X_set = set(X)
        
        H2 = True
        for c in classes_gt_1:
            if len(X_set.intersection(c)) != 1:
                H2 = False
                break
                
        if H2 and len(X) != len(classes_gt_1):
            H2 = False
    except Exception:
        H2 = False

    # H3: C_G(x_i) is the centralizer of x_i in G
    try:
        H3 = True
        if len(X) != len(C):
            H3 = False
        else:
            elements = list(G.elements)
            for x, c_sub in zip(X, C):
                actual_c = set()
                for g in elements:
                    if g * x == x * g:
                        actual_c.add(g)
                
                if hasattr(c_sub, 'elements'):
                    c_set = set(c_sub.elements)
                else:
                    c_set = set(c_sub)
                    
                if c_set != actual_c:
                    H3 = False
                    break
    except Exception:
        H3 = False

    # neg_Q: |G| != |Z(G)| + sum_{i=1}^k [G : C_G(x_i)]
    try:
        elements = list(G.elements)
        Z_G = set()
        for g in elements:
            if all(g * h == h * g for h in elements):
                Z_G.add(g)
                
        sum_index = 0
        for c_sub in C:
            if hasattr(c_sub, 'elements'):
                c_len = len(list(c_sub.elements))
            else:
                c_len = len(c_sub)
            sum_index += len(elements) // c_len
            
        Q = (len(elements) == len(Z_G) + sum_index)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: {x_1, ..., x_k} is a complete set of representatives of the distinct conjugacy classes of G of size greater than 1",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "¬Q: |G| != |Z(G)| + sum_{i=1}^k (G : C_G(x_i))"
]

N_HYP = 3
NEG_Q_INDEX = 3