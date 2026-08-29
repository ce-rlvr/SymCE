import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def are_isomorphic(table1, table2):
    k = len(table1)
    if len(table2) != k:
        return False
    if k == 1:
        return True
    
    id1 = None
    for i in range(k):
        if all(table1[i][j] == j for j in range(k)):
            id1 = i
            break
    id2 = None
    for i in range(k):
        if all(table2[i][j] == j for j in range(k)):
            id2 = i
            break
            
    if id1 is None or id2 is None:
        return False
        
    def get_orders(table, id_elem):
        orders = []
        for i in range(k):
            curr = i
            order = 1
            while curr != id_elem and order <= k:
                curr = table[curr][i]
                order += 1
            orders.append(order)
        return orders
        
    orders1 = get_orders(table1, id1)
    orders2 = get_orders(table2, id2)
    if sorted(orders1) != sorted(orders2):
        return False
        
    elements_by_order1 = {}
    elements_by_order2 = {}
    for i, o in enumerate(orders1):
        elements_by_order1.setdefault(o, []).append(i)
    for i, o in enumerate(orders2):
        elements_by_order2.setdefault(o, []).append(i)
        
    choices = []
    for i in range(k):
        if i == id1:
            choices.append([id2])
        else:
            choices.append(elements_by_order2.get(orders1[i], []))
            
    mapping = [None] * k
    used = [False] * k
    
    def search(idx):
        if idx == k:
            return True
        for c in choices[idx]:
            if not used[c]:
                mapping[idx] = c
                used[c] = True
                
                consistent = True
                for i in range(idx + 1):
                    for j in range(idx + 1):
                        prod1 = table1[i][j]
                        prod2 = table2[mapping[i]][mapping[j]]
                        if prod1 <= idx:
                            if prod2 != mapping[prod1]:
                                consistent = False
                                break
                        else:
                            if used[prod2]:
                                consistent = False
                                break
                    if not consistent:
                        break
                        
                if consistent:
                    if search(idx + 1):
                        return True
                        
                mapping[idx] = None
                used[c] = False
        return False

    return search(0)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            alpha = witness['alpha']
        else:
            G, N, alpha = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    try:
        G_elements = list(G.generate())
        N_elements = list(N.generate())
        
        alpha_N_elements = set()
        for n in N_elements:
            if callable(alpha):
                val = alpha(n)
            else:
                val = alpha[n]
            alpha_N_elements.add(val)
            
        if not alpha_N_elements.issubset(set(G_elements)):
            neg_q = True
        else:
            id_elem = None
            for g in G_elements:
                if g * g == g:
                    id_elem = g
                    break
                    
            is_group = True
            if id_elem not in alpha_N_elements:
                is_group = False
            else:
                for a in alpha_N_elements:
                    if a**-1 not in alpha_N_elements:
                        is_group = False
                        break
                    for b in alpha_N_elements:
                        if a*b not in alpha_N_elements:
                            is_group = False
                            break
                    if not is_group:
                        break
            
            if not is_group:
                neg_q = True
            else:
                alpha_N_group = PermutationGroup(list(alpha_N_elements))
                if not alpha_N_group.is_normal(G):
                    neg_q = True
                else:
                    def get_quotient_table(Grp, Subgrp):
                        Grp_elems = list(Grp.generate())
                        Subgrp_elems = list(Subgrp.generate())
                        cosets = []
                        for g in Grp_elems:
                            c = frozenset(g * n for n in Subgrp_elems)
                            if c not in cosets:
                                cosets.append(c)
                        k = len(cosets)
                        table = [[0]*k for _ in range(k)]
                        for i in range(k):
                            for j in range(k):
                                rep_i = next(iter(cosets[i]))
                                rep_j = next(iter(cosets[j]))
                                prod = rep_i * rep_j
                                for m in range(k):
                                    if prod in cosets[m]:
                                        table[i][j] = m
                                        break
                        return table

                    table_N = get_quotient_table(G, N)
                    table_alpha_N = get_quotient_table(G, alpha_N_group)
                    
                    if are_isomorphic(table_N, table_alpha_N):
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: alpha(N) is not a normal subgroup of G, or G/N is not isomorphic to G/alpha(N)"
]
N_HYP = 2
NEG_Q_INDEX = 2