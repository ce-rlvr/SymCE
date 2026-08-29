import sympy
from sympy.combinatorics import PermutationGroup, CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, S = witness
    except Exception:
        return [False, False]
        
    # H_1: S is a generating set of G consisting of a single element and its inverse
    try:
        S_list = list(S)
        if len(S_list) == 0:
            h1 = False
        else:
            s = S_list[0]
            if set(S_list) == {s, s**-1}:
                H = PermutationGroup(S_list)
                h1 = bool(H.order() == G.order() and H.is_subgroup(G))
            else:
                h1 = False
    except Exception:
        h1 = False
        
    # ¬Q: The Cayley graph Gamma(G, S) is not isomorphic to the cycle graph C_n
    try:
        n = G.order()
        try:
            elements = list(G.elements)
        except AttributeError:
            elements = list(G.generate())
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        adj = {i: [] for i in range(n)}
        for g in elements:
            u = elem_to_idx[g]
            for s_elem in set(S_list):
                gs = g * s_elem
                v = elem_to_idx[gs]
                adj[u].append(v)
                
        is_Cn = False
        if n >= 3:
            is_2_regular = True
            for u in range(n):
                neighbors = set(adj[u])
                # A cycle graph C_n must be a simple 2-regular graph
                if len(neighbors) != 2 or u in neighbors:
                    is_2_regular = False
                    break
            if is_2_regular:
                # Check connectivity
                visited = set()
                stack = [0]
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        stack.extend(adj[node])
                if len(visited) == n:
                    is_Cn = True
                    
        neg_q = not is_Cn
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is a generating set of G consisting of a single element and its inverse",
    "¬Q: The Cayley graph Gamma(G, S) is not isomorphic to the cycle graph C_n"
]

N_HYP = 1
NEG_Q_INDEX = 1