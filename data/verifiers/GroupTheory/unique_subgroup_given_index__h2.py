import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
            G, H, n_wit = witness
        elif len(witness) == 2:
            G, H = witness
            n_wit = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = hasattr(G, 'elements') or hasattr(G, 'generate_dimino')
        if hasattr(G, 'is_group'):
            h1 = h1 and G.is_group
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G of index n
    try:
        G_els = frozenset(G.generate_dimino()) if hasattr(G, 'generate_dimino') else frozenset(G.elements)
        H_els = frozenset(H.generate_dimino()) if hasattr(H, 'generate_dimino') else frozenset(H.elements)
        
        id_el = None
        for e in G_els:
            if e * e == e:
                id_el = e
                break
        if id_el is None:
            id_el = list(G_els)[0]
            
        is_subgroup = True
        if id_el not in H_els:
            is_subgroup = False
        else:
            for a in H_els:
                for b in H_els:
                    if a * b not in H_els:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        h2 = H_els.issubset(G_els) and is_subgroup and len(G_els) % len(H_els) == 0
        n = len(G_els) // len(H_els) if len(H_els) > 0 else 0
        if n_wit is not None:
            h2 = h2 and (n == n_wit)
    except Exception:
        h2 = False
        n = None
        id_el = None
        G_els = frozenset()
        H_els = frozenset()
        
    # H3: For any subgroup K of G, if the index of K in G is n, then K = H
    try:
        if not h2:
            h3 = False
        else:
            if hasattr(G, 'subgroups'):
                subs = G.subgroups()
                h3 = True
                for K in subs:
                    K_els = frozenset(K.generate_dimino()) if hasattr(K, 'generate_dimino') else frozenset(K.elements)
                    if len(G_els) // len(K_els) == n:
                        if K_els != H_els:
                            h3 = False
                            break
            else:
                subgroups = {frozenset([id_el])}
                for x in G_els:
                    if x == id_el:
                        continue
                    new_subs = set()
                    for S_els in subgroups:
                        if x in S_els:
                            continue
                        
                        closure = set(S_els)
                        queue = [x]
                        closure.add(x)
                        
                        while queue:
                            curr = queue.pop()
                            to_add = set()
                            for a in closure:
                                c1 = a * curr
                                if c1 not in closure:
                                    to_add.add(c1)
                                c2 = curr * a
                                if c2 not in closure:
                                    to_add.add(c2)
                            queue.extend(to_add)
                            closure.update(to_add)
                            
                        K_els = frozenset(closure)
                        if K_els not in subgroups and K_els not in new_subs:
                            new_subs.add(K_els)
                    subgroups.update(new_subs)
                    
                h3 = True
                for K_els in subgroups:
                    if len(G_els) // len(K_els) == n:
                        if K_els != H_els:
                            h3 = False
                            break
    except Exception:
        h3 = False
        
    # neg_Q: H is not a normal subgroup of G
    try:
        if not h2:
            neg_q = False
        else:
            is_normal = True
            for g in G_els:
                g_inv = ~g if hasattr(g, '__invert__') else None
                if g_inv is None:
                    for e in G_els:
                        if g * e == id_el:
                            g_inv = e
                            break
                for h in H_els:
                    if g * h * g_inv not in H_els:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G of index n",
    "H_3: For any subgroup K of G, if the index of K in G is n, then K = H",
    "not Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3