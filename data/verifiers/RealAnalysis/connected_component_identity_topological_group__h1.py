import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G = list(witness['G'])
        op_val = witness['op']
        if callable(op_val):
            op = op_val
        elif isinstance(op_val, dict):
            op = lambda x, y: op_val[(x, y)]
        else:
            op = lambda x, y: op_val[x][y]
        
        topology = set(frozenset(u) for u in witness['topology'])
        e = witness['e']
        C = set(witness['C'])
    except Exception:
        return [False, False, False]

    # H1: e is the identity element of G
    try:
        h1 = True
        if e not in G:
            h1 = False
        else:
            for x in G:
                if op(e, x) != x or op(x, e) != x:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: C is the connected component of G containing e
    try:
        G_set = frozenset(G)
        if frozenset() not in topology or G_set not in topology:
            h2 = False
        else:
            valid_top = True
            for u in topology:
                for v in topology:
                    if u.intersection(v) not in topology:
                        valid_top = False
                        break
                if not valid_top:
                    break
            if valid_top:
                for u in topology:
                    for v in topology:
                        if u.union(v) not in topology:
                            valid_top = False
                            break
                    if not valid_top:
                        break
            
            if not valid_top:
                h2 = False
            else:
                # In a finite topological space, connected components correspond to the 
                # connected components of the underlying graph of its specialization preorder.
                # x ~ y if x is in the closure of {y} or y is in the closure of {x}.
                adj = {x: set() for x in G}
                for x in G:
                    for y in G:
                        if x == y: continue
                        x_in_cl_y = True
                        for U in topology:
                            if x in U and y not in U:
                                x_in_cl_y = False
                                break
                        if x_in_cl_y:
                            adj[x].add(y)
                            adj[y].add(x)
                
                comp = set([e])
                queue = [e]
                while queue:
                    curr = queue.pop(0)
                    for neighbor in adj[curr]:
                        if neighbor not in comp:
                            comp.add(neighbor)
                            queue.append(neighbor)
                h2 = (C == comp)
    except Exception:
        h2 = False

    # neg_Q: C is NOT a closed normal subgroup of G
    try:
        is_closed = (G_set - C) in topology

        is_subgroup = True
        if e not in C:
            is_subgroup = False
        else:
            for x in C:
                for y in C:
                    if op(x, y) not in C:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            if is_subgroup:
                for x in C:
                    inv_x = None
                    for y in G:
                        if op(x, y) == e and op(y, x) == e:
                            inv_x = y
                            break
                    if inv_x is None or inv_x not in C:
                        is_subgroup = False
                        break

        is_normal = True
        if is_subgroup:
            for g in G:
                inv_g = None
                for y in G:
                    if op(g, y) == e and op(y, g) == e:
                        inv_g = y
                        break
                if inv_g is None:
                    is_normal = False
                    break
                for x in C:
                    conj = op(g, op(x, inv_g))
                    if conj not in C:
                        is_normal = False
                        break
                if not is_normal:
                    break

        Q = is_closed and is_subgroup and is_normal
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: e is the identity element of G",
    "H_2: C is the connected component of G containing e",
    "¬Q: C is not a closed normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2