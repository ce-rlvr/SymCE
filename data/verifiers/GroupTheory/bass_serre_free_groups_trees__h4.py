import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        if len(witness) != 3:
            return [False, False, False, False]
        G, V, E = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: T is a tree
    try:
        V_set = set(V)
        if len(V_set) == 0:
            h2 = False
        else:
            edges = []
            for e in E:
                e_list = list(e)
                if len(e_list) != 2:
                    raise ValueError
                edges.append(set(e_list))
            
            if len(edges) != len(V_set) - 1:
                h2 = False
            else:
                adj = {v: [] for v in V_set}
                for u, v in edges:
                    adj[u].append(v)
                    adj[v].append(u)
                
                visited = set()
                start_node = next(iter(V_set))
                stack = [start_node]
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        stack.extend(adj[node])
                
                h2 = len(visited) == len(V_set)
    except Exception:
        h2 = False

    # H_3: G acts freely on the vertices and edges of T
    try:
        h3 = True
        edges_list_of_sets = [set(e) for e in E]
        for g in G.elements:
            # Check that g acts as an automorphism of the tree T
            for e in edges_list_of_sets:
                u, v = list(e)
                if {g(u), g(v)} not in edges_list_of_sets:
                    h3 = False
                    break
            if not h3:
                break
            
            if g.is_Identity:
                continue
                
            # Check free action on vertices
            for v in V_set:
                if g(v) == v:
                    h3 = False
                    break
            if not h3:
                break
            
            # Check free action on oriented edges
            for e in edges_list_of_sets:
                u, v = list(e)
                if g(u) == u and g(v) == v:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # ¬Q: G is not a free group
    try:
        # A finite group is free if and only if it is the trivial group.
        # Since G is a PermutationGroup, it is finite.
        neg_q = G.order() > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: T is a tree",
    "H_3: G acts freely on the vertices and edges of T",
    "¬Q: G is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3