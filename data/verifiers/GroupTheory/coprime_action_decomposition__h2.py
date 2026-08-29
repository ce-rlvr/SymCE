import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def get_group_info(G):
    if isinstance(G, tuple) and len(G) == 4:
        return G[0], G[1], G[2], G[3], False
    
    if hasattr(G, 'elements'):
        elements = list(G.elements)
    elif hasattr(G, 'generate'):
        elements = list(G.generate())
    else:
        raise ValueError("Invalid group format")
        
    op = lambda x, y: x * y
    inv = lambda x: x**-1
    
    if not elements:
        return [], op, inv, None, False
        
    id_el = elements[0]
    for e in elements:
        is_id = True
        for x in elements:
            if e * x != x:
                is_id = False
                break
        if is_id:
            id_el = e
            break
            
    return elements, op, inv, id_el, True

def is_group(elements, op, inv, id_el):
    if not elements: return False
    if id_el not in elements: return False
    for a in elements:
        if op(id_el, a) != a or op(a, id_el) != a: return False
        if op(a, inv(a)) != id_el or op(inv(a), a) != id_el: return False
        for b in elements:
            ab = op(a, b)
            if ab not in elements: return False
            for c in elements:
                if op(ab, c) != op(a, op(b, c)): return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, A, action = witness
        G_els, G_op, G_inv, G_id, G_known = get_group_info(G)
        A_els, A_op, A_inv, A_id, A_known = get_group_info(A)
        
        if len(G_els) > 1000 or len(A_els) > 1000:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
        if not G_known:
            h1 = is_group(G_els, G_op, G_inv, G_id)
        if len(G_els) == 0: h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        if not A_known:
            if not is_group(A_els, A_op, A_inv, A_id):
                h2 = False
        
        if h2:
            for g in G_els:
                for a in A_els:
                    if action(g, a) not in A_els:
                        h2 = False
                        break
                if not h2: break
                
                for a in A_els:
                    for b in A_els:
                        if action(g, A_op(a, b)) != A_op(action(g, a), action(g, b)):
                            h2 = False
                            break
                    if not h2: break
                    
        if h2:
            for g1 in G_els:
                for g2 in G_els:
                    for a in A_els:
                        if action(G_op(g1, g2), a) != action(g1, action(g2, a)):
                            h2 = False
                            break
                    if not h2: break
                    
        if h2:
            for a in A_els:
                if action(G_id, a) != a:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(len(G_els), len(A_els)) == 1
    except Exception:
        h3 = False

    try:
        C_A = []
        for a in A_els:
            if all(action(g, a) == a for g in G_els):
                C_A.append(a)
                
        generators = []
        for g in G_els:
            for a in A_els:
                gen = A_op(action(g, a), A_inv(a))
                if gen not in generators:
                    generators.append(gen)
                
        GA_subgroup = []
        for gen in generators:
            if gen not in GA_subgroup:
                GA_subgroup.append(gen)
        if A_id not in GA_subgroup:
            GA_subgroup.append(A_id)
            
        added = True
        while added:
            added = False
            new_els = []
            for x in GA_subgroup:
                for y in GA_subgroup:
                    xy = A_op(x, y)
                    if xy not in GA_subgroup and xy not in new_els:
                        new_els.append(xy)
            if new_els:
                GA_subgroup.extend(new_els)
                added = True
                
        def is_normal(subgroup, elements, op, inv):
            for h in subgroup:
                for a in elements:
                    conj = op(op(a, h), inv(a))
                    if conj not in subgroup:
                        return False
            return True
            
        is_dp = True
        if not is_normal(C_A, A_els, A_op, A_inv):
            is_dp = False
        if not is_normal(GA_subgroup, A_els, A_op, A_inv):
            is_dp = False
            
        intersection = [x for x in C_A if x in GA_subgroup]
        if len(intersection) != 1 or intersection[0] != A_id:
            is_dp = False
            
        if len(C_A) * len(GA_subgroup) != len(A_els):
            is_dp = False
            
        neg_q = not is_dp
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts on A by group automorphisms",
    "H_3: The orders of G and A are coprime",
    "neg_Q: A does not decompose as the direct sum of C_A(G) and the commutator of G and A"
]

N_HYP = 3
NEG_Q_INDEX = 3