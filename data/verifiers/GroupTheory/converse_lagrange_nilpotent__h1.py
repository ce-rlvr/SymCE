import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
        G, d = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a nilpotent group
    try:
        is_nilp = G.is_nilpotent
        if callable(is_nilp):
            is_nilp = is_nilp()
        h1 = bool(is_nilp)
    except Exception:
        h1 = False
        
    # H_2: d is a positive integer that divides the order of G
    try:
        g_order = G.order
        if callable(g_order):
            g_order = g_order()
            
        is_valid_d = (isinstance(d, int) and not isinstance(d, bool)) or isinstance(d, sympy.Integer)
        if g_order == sympy.oo:
            h2 = False
        elif is_valid_d and d > 0 and g_order % d == 0:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: G does not contain a subgroup of order d
    try:
        g_order = G.order
        if callable(g_order):
            g_order = g_order()
            
        is_valid_d = (isinstance(d, int) and not isinstance(d, bool)) or isinstance(d, sympy.Integer)
        
        if g_order == sympy.oo:
            neg_q = False
        elif not is_valid_d or d <= 0:
            neg_q = False
        elif g_order % d != 0:
            neg_q = True
        elif d == 1 or d == g_order:
            neg_q = False
        elif g_order > 5000:
            neg_q = False
        else:
            has_subgroup = False
            elements = list(G.elements)
            try:
                id_el = G.identity
            except AttributeError:
                for e in elements:
                    if e * e == e:
                        id_el = e
                        break
                        
            cyclic_subgroups = set()
            for g in elements:
                sub = {id_el}
                curr = g
                while curr != id_el:
                    sub.add(curr)
                    curr = curr * g
                if d % len(sub) == 0:
                    cyclic_subgroups.add(frozenset(sub))
                    
            for sub in cyclic_subgroups:
                if len(sub) == d:
                    has_subgroup = True
                    break
                    
            if not has_subgroup:
                known_subgroups = set(cyclic_subgroups)
                new_subgroups = set(cyclic_subgroups)
                
                while new_subgroups and not has_subgroup:
                    next_new = set()
                    for H1 in new_subgroups:
                        for H2 in known_subgroups:
                            if H1.issubset(H2) or H2.issubset(H1):
                                continue
                                
                            sub = set(H1)
                            sub.update(H2)
                            
                            queue = list(sub)
                            idx = 0
                            invalid = False
                            while idx < len(queue):
                                a = queue[idx]
                                idx += 1
                                current_sub = list(sub)
                                for b in current_sub:
                                    c = a * b
                                    if c not in sub:
                                        sub.add(c)
                                        queue.append(c)
                                        if len(sub) > d:
                                            invalid = True
                                            break
                                    c2 = b * a
                                    if c2 not in sub:
                                        sub.add(c2)
                                        queue.append(c2)
                                        if len(sub) > d:
                                            invalid = True
                                            break
                                if invalid:
                                    break
                                    
                            if invalid or d % len(sub) != 0:
                                continue
                                
                            sub_fs = frozenset(sub)
                            if len(sub_fs) == d:
                                has_subgroup = True
                                break
                                
                            if sub_fs not in known_subgroups and sub_fs not in next_new:
                                next_new.add(sub_fs)
                                
                        if has_subgroup:
                            break
                    known_subgroups.update(next_new)
                    new_subgroups = next_new
                    
            neg_q = not has_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: d is a positive integer that divides the order of G",
    "¬Q: G does not contain at least one subgroup of order d"
]

N_HYP = 2
NEG_Q_INDEX = 2