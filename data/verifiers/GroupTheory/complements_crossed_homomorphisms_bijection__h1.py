import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_closure(generators, identity):
    closure = set(generators)
    closure.add(identity)
    queue = list(closure)
    while queue:
        curr = queue.pop(0)
        new_elements = set()
        for x in closure:
            p1 = curr * x
            if p1 not in closure:
                new_elements.add(p1)
            p2 = x * curr
            if p2 not in closure:
                new_elements.add(p2)
        for elem in new_elements:
            closure.add(elem)
            queue.append(elem)
    return frozenset(closure)

def get_all_subgroups(G):
    identity = G.identity
    elements = list(G.elements)
    subgroups = {frozenset([identity])}
    
    cyclic_subgroups = set()
    for g in elements:
        cyclic_subgroups.add(get_closure([g], identity))
        
    subgroups.update(cyclic_subgroups)
    
    active = list(cyclic_subgroups)
    while active:
        new_active = []
        for sg1 in active:
            for sg2 in subgroups:
                if not sg1.issubset(sg2) and not sg2.issubset(sg1):
                    merged = get_closure(sg1 | sg2, identity)
                    if merged not in subgroups:
                        subgroups.add(merged)
                        new_active.append(merged)
                        if len(subgroups) > 1000:
                            return subgroups
        active = new_active
        
    return subgroups

def count_complements(G, N_elements):
    G_elements = list(G.elements)
    k = len(G_elements) // len(N_elements)
    if len(G_elements) % len(N_elements) != 0:
        return 0
    subgroups = get_all_subgroups(G)
    count = 0
    for sg in subgroups:
        if len(sg) == k:
            intersect = sg.intersection(N_elements)
            if len(intersect) == 1:
                count += 1
    return count

def count_Z1(G, N_elements):
    cosets = []
    element_to_coset = {}
    for g in list(G.elements):
        if g not in element_to_coset:
            coset = set()
            for n in N_elements:
                gn = g * n
                coset.add(gn)
                element_to_coset[gn] = len(cosets)
            cosets.append(g)
            
    Q_size = len(cosets)
    Q_mul = {}
    action = {}
    
    for i in range(Q_size):
        Q_mul[i] = {}
        action[i] = {}
        x = cosets[i]
        for j in range(Q_size):
            y = cosets[j]
            xy = x * y
            Q_mul[i][j] = element_to_coset[xy]
        for n in N_elements:
            action[i][n] = x * n * ~x
            
    valid_f_count = 0
    f = [None] * Q_size
    f[0] = G.identity
    N_list = list(N_elements)
    
    def search(idx):
        nonlocal valid_f_count
        if idx == Q_size:
            valid_f_count += 1
            return
            
        for n in N_list:
            f[idx] = n
            ok = True
            for i in range(idx + 1):
                for j in range(idx + 1):
                    k = Q_mul[i][j]
                    if k <= idx:
                        if f[k] != f[i] * action[i][f[j]]:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                search(idx + 1)
                
    search(1)
    return valid_f_count

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, H = witness
            elif len(witness) == 2:
                G, N = witness
                H = None
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: N is an abelian group
    try:
        h1 = N.is_abelian
        if callable(h1):
            h1 = h1()
    except Exception:
        h1 = False
        
    # neg_Q: The bijective correspondence fails
    try:
        neg_q = False
        G_elements = list(G.elements)
        
        is_sub_N = True
        for gen in N.generators:
            if gen not in G_elements:
                is_sub_N = False
                break
                
        if not is_sub_N:
            neg_q = True
        else:
            N_elements = set(N.elements)
            
            is_normal = True
            for g in G_elements:
                for n in N_elements:
                    if g * n * ~g not in N_elements:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
            if not is_normal:
                # If N is not normal, the action is undefined, so Z^1 is undefined
                neg_q = True
            else:
                num_complements = count_complements(G, N_elements)
                
                if H is not None:
                    is_sub_H = True
                    for gen in H.generators:
                        if gen not in G_elements:
                            is_sub_H = False
                            break
                            
                    if not is_sub_H:
                        neg_q = True
                    elif len(N_elements) * len(list(H.elements)) != len(G_elements):
                        neg_q = True
                    else:
                        intersect = set(H.elements).intersection(N_elements)
                        if len(intersect) != 1:
                            neg_q = True
                        else:
                            z1_size = count_Z1(G, N_elements)
                            if num_complements != z1_size:
                                neg_q = True
                            else:
                                neg_q = False
                else:
                    z1_size = count_Z1(G, N_elements)
                    if num_complements != z1_size:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "¬Q: The bijective correspondence between complements of N and Z^1(H, N) fails"
]
N_HYP = 1
NEG_Q_INDEX = 1