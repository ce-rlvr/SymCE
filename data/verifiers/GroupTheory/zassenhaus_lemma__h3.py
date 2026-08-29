import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(H, G):
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        elems_G = set(G.elements)
        for gen in H.generators:
            if gen not in elems_G:
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G):
            return False
        elems_G = list(G.elements)
        elems_N = set(N.elements)
        for g in elems_G:
            g_inv = g**-1
            for n in elems_N:
                if g * n * g_inv not in elems_N:
                    return False
        return True
    except Exception:
        return False

def intersection(H, K):
    try:
        elems_H = set(H.elements)
        elems_K = set(K.elements)
        common = list(elems_H.intersection(elems_K))
        return PermutationGroup(common)
    except Exception:
        return None

def product_group(H, K):
    try:
        if H is None or K is None:
            return None
        elems_H = set(H.elements)
        elems_K = set(K.elements)
        prod_set = set(h * k for h in elems_H for k in elems_K)
        
        gen_group = PermutationGroup(list(elems_H) + list(elems_K))
        
        if gen_group.order() == len(prod_set):
            return gen_group
        return None
    except Exception:
        return None

def quotient_group_table(G, N):
    try:
        if not is_normal(N, G):
            return None
            
        elems_G = list(G.elements)
        elems_N = set(N.elements)
        
        cosets = []
        coset_reps = []
        seen = set()
        for g in elems_G:
            if g not in seen:
                coset = frozenset(g * n for n in elems_N)
                cosets.append(coset)
                coset_reps.append(g)
                seen.update(coset)
                
        coset_to_idx = {c: i for i, c in enumerate(cosets)}
        n_cosets = len(cosets)
        table = [[0]*n_cosets for _ in range(n_cosets)]
        for i in range(n_cosets):
            for j in range(n_cosets):
                prod_rep = coset_reps[i] * coset_reps[j]
                prod_coset = frozenset(prod_rep * n for n in elems_N)
                if prod_coset not in coset_to_idx:
                    return None
                table[i][j] = coset_to_idx[prod_coset]
        return table
    except Exception:
        return None

def are_isomorphic(table1, table2):
    try:
        n = len(table1)
        if len(table2) != n:
            return False
        if n == 1:
            return True
            
        id1 = next(i for i in range(n) if all(table1[i][j] == j for j in range(n)))
        id2 = next(i for i in range(n) if all(table2[i][j] == j for j in range(n)))
        
        def get_orders(table, id_elem):
            orders = []
            for i in range(n):
                curr = i
                order = 1
                while curr != id_elem:
                    curr = table[curr][i]
                    order += 1
                    if order > n:
                        break
                orders.append(order)
            return orders
            
        orders1 = get_orders(table1, id1)
        orders2 = get_orders(table2, id2)
        if sorted(orders1) != sorted(orders2):
            return False
            
        cands = []
        for i in range(n):
            if i == id1:
                cands.append([id2])
            else:
                cands.append([j for j in range(n) if orders1[i] == orders2[j] and j != id2])
                
        mapping = [None] * n
        
        def search(idx, used):
            if idx == n:
                return True
            for cand in cands[idx]:
                if cand not in used:
                    mapping[idx] = cand
                    valid = True
                    for i in range(idx + 1):
                        p1 = table1[i][idx]
                        if p1 <= idx:
                            if mapping[p1] != table2[mapping[i]][cand]:
                                valid = False
                                break
                        p2 = table1[idx][i]
                        if p2 <= idx:
                            if mapping[p2] != table2[cand][mapping[i]]:
                                valid = False
                                break
                    if valid:
                        used.add(cand)
                        if search(idx + 1, used):
                            return True
                        used.remove(cand)
            return False
            
        return search(0, set())
    except Exception:
        return False

def evaluate_conclusion(G, A, A_star, B, B_star):
    try:
        A_int_B = intersection(A, B)
        A_int_B_star = intersection(A, B_star)
        A_star_int_B = intersection(A_star, B)
        
        L_num = product_group(A_int_B, A_star)
        L_den = product_group(A_int_B_star, A_star)
        R_num = product_group(A_int_B, B_star)
        R_den = product_group(A_star_int_B, B_star)
        
        if L_num is None or L_den is None or R_num is None or R_den is None:
            return False
            
        table_L = quotient_group_table(L_num, L_den)
        table_R = quotient_group_table(R_num, R_den)
        
        if table_L is None or table_R is None:
            return False
            
        return are_isomorphic(table_L, table_R)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        G, A, A_star, B, B_star = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h2 = False
        
    try:
        h3 = is_normal(B_star, B)
    except Exception:
        h3 = False
        
    try:
        q = evaluate_conclusion(G, A, A_star, B, B_star)
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A and B are subgroups of G",
    "H_3: B^* is a normal subgroup of B",
    "¬Q: (A \\cap B)A^* / (A \\cap B^*)A^* \\cong (A \\cap B)B^* / (A^* \\cap B)B^* fails"
]

N_HYP = 3
NEG_Q_INDEX = 3