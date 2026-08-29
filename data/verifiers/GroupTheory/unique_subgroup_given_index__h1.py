import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros
import itertools
import functools
import math

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

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return frozenset(obj.elements)
    elif hasattr(obj, 'generate'):
        return frozenset(obj.generate())
    else:
        return frozenset(obj)

def check_c1(witness):
    try:
        G, H, n = witness
        return int(n) == n and n > 0
    except Exception:
        return False

def check_c2(witness):
    try:
        G, H, n = witness
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        if not H_elems.issubset(G_elems):
            return False
        if len(H_elems) == 0:
            return False
        
        elem = next(iter(G_elems))
        id_el = elem ** 0
        if id_el not in H_elems:
            return False
            
        for a in H_elems:
            for b in H_elems:
                if a * b not in H_elems:
                    return False
                    
        if len(G_elems) % len(H_elems) != 0:
            return False
        return len(G_elems) // len(H_elems) == n
    except Exception:
        return False

def check_c3(witness):
    try:
        G, H, n = witness
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        if len(G_elems) % n != 0:
            return True
            
        target_size = len(G_elems) // n
        
        for g in G_elems:
            g_inv = g ** -1
            K_elems = frozenset({g * h * g_inv for h in H_elems})
            if len(K_elems) == target_size and K_elems != H_elems:
                return False
                
        cyclic_subgroups = set()
        for g in G_elems:
            cg = set()
            curr = g
            while curr not in cg:
                cg.add(curr)
                curr = curr * g
            cyclic_subgroups.add(frozenset(cg))
            
        subgroups = set(cyclic_subgroups)
        queue = list(cyclic_subgroups)
        
        while queue:
            curr_H = queue.pop(0)
            for C in cyclic_subgroups:
                if not C.issubset(curr_H):
                    S = curr_H | C
                    gen = set(S)
                    frontier = list(S)
                    while frontier:
                        new_frontier = []
                        for a in frontier:
                            for b in gen:
                                p = a * b
                                if p not in gen:
                                    gen.add(p)
                                    new_frontier.append(p)
                        frontier = new_frontier
                    fs = frozenset(gen)
                    if fs not in subgroups:
                        subgroups.add(fs)
                        queue.append(fs)
                        
        for K in subgroups:
            if len(K) == target_size and K != H_elems:
                return False
                
        return True
    except Exception:
        return False

def check_c4(witness):
    try:
        G, H, n = witness
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        for g in G_elems:
            g_inv = g ** -1
            K_elems = frozenset({g * h * g_inv for h in H_elems})
            if K_elems != H_elems:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [
        check_c1(witness),
        check_c2(witness),
        check_c3(witness),
        check_c4(witness)
    ]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: H is a subgroup of G of index n",
    "H_3: For any subgroup K of G, if the index of K in G is n, then K = H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3