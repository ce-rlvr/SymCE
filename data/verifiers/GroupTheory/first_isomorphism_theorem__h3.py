import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def are_isomorphic(elements1, mul1, id1, elements2, mul2, id2):
    if len(elements1) != len(elements2):
        return False
    if len(elements1) == 1:
        return True
    
    n = len(elements1)
    idx1 = {e: i for i, e in enumerate(elements1)}
    idx2 = {e: i for i, e in enumerate(elements2)}
    
    table1 = [[idx1[mul1(a, b)] for b in elements1] for a in elements1]
    table2 = [[idx2[mul2(a, b)] for b in elements2] for a in elements2]
    
    def get_orders(elements, table, id_idx):
        orders = []
        for i in range(n):
            curr = i
            order = 1
            while curr != id_idx:
                curr = table[curr][i]
                order += 1
                if order > n:
                    break
            orders.append(order)
        return orders
    
    id1_idx = idx1[id1]
    id2_idx = idx2[id2]
    
    orders1 = get_orders(elements1, table1, id1_idx)
    orders2 = get_orders(elements2, table2, id2_idx)
    
    by_order1 = {}
    by_order2 = {}
    for i, o in enumerate(orders1):
        by_order1.setdefault(o, []).append(i)
    for i, o in enumerate(orders2):
        by_order2.setdefault(o, []).append(i)
        
    if set(by_order1.keys()) != set(by_order2.keys()):
        return False
    for o in by_order1:
        if len(by_order1[o]) != len(by_order2[o]):
            return False
            
    mapping = {}
    mapped_targets = set()
    
    def backtrack(idx):
        if idx == n:
            for i in range(n):
                for j in range(n):
                    if mapping[table1[i][j]] != table2[mapping[i]][mapping[j]]:
                        return False
            return True
        
        if idx in mapping:
            return backtrack(idx + 1)
            
        order_u = orders1[idx]
        for v in by_order2.get(order_u, []):
            if v not in mapped_targets:
                consistent = True
                for mapped_u, mapped_v in mapping.items():
                    prod1 = table1[idx][mapped_u]
                    if prod1 in mapping and mapping[prod1] != table2[v][mapped_v]:
                        consistent = False
                        break
                    prod1 = table1[mapped_u][idx]
                    if prod1 in mapping and mapping[prod1] != table2[mapped_v][v]:
                        consistent = False
                        break
                if not consistent:
                    continue
                    
                mapping[idx] = v
                mapped_targets.add(v)
                if backtrack(idx + 1):
                    return True
                del mapping[idx]
                mapped_targets.remove(v)
        return False

    mapping[id1_idx] = id2_idx
    mapped_targets.add(id2_idx)
    return backtrack(0)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        G, H, phi = witness
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        G, H, phi = witness
        
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            if callable(phi):
                phi_dict = {}
                for g in G_elements:
                    phi_dict[g] = phi(g)
                phi = phi_dict
                
            if not isinstance(phi, dict):
                neg_q = False
            elif not all(g in phi for g in G_elements):
                neg_q = False
            elif not all(phi[g] in H_elements for g in G_elements):
                neg_q = False
            else:
                id_H = None
                for h in H_elements:
                    if h * h == h:
                        id_H = h
                        break
                
                if id_H is None:
                    neg_q = False
                else:
                    ker_elements = [g for g in G_elements if phi[g] == id_H]
                    
                    if not ker_elements:
                        neg_q = True
                    else:
                        is_subgroup = True
                        for a in ker_elements:
                            for b in ker_elements:
                                if a * b not in ker_elements:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                        
                        if not is_subgroup:
                            neg_q = True
                        else:
                            is_normal = True
                            for g in G_elements:
                                g_inv = g**-1
                                for k in ker_elements:
                                    if g * k * g_inv not in ker_elements:
                                        is_normal = False
                                        break
                                if not is_normal:
                                    break
                            
                            if not is_normal:
                                neg_q = True
                            else:
                                phi_G_elements = set(phi[g] for g in G_elements)
                                
                                is_phi_G_subgroup = True
                                for a in phi_G_elements:
                                    for b in phi_G_elements:
                                        if a * b not in phi_G_elements:
                                            is_phi_G_subgroup = False
                                            break
                                    if not is_phi_G_subgroup:
                                        break
                                
                                if not is_phi_G_subgroup:
                                    neg_q = True
                                else:
                                    if len(G_elements) // len(ker_elements) != len(phi_G_elements):
                                        neg_q = True
                                    else:
                                        cosets = []
                                        for g in G_elements:
                                            c = frozenset(g * k for k in ker_elements)
                                            if c not in cosets:
                                                cosets.append(c)
                                                
                                        def mul1(c1, c2):
                                            rep1 = next(iter(c1))
                                            rep2 = next(iter(c2))
                                            prod = rep1 * rep2
                                            for c in cosets:
                                                if prod in c:
                                                    return c
                                            return cosets[0]
                                            
                                        id1 = frozenset(ker_elements)
                                        
                                        elements2 = list(phi_G_elements)
                                        def mul2(e1, e2):
                                            return e1 * e2
                                        id2 = id_H
                                        
                                        if are_isomorphic(cosets, mul1, id1, elements2, mul2, id2):
                                            neg_q = False
                                        else:
                                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "¬Q: ker(phi) is not a normal subgroup of G, or G/ker(phi) is not isomorphic to phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2