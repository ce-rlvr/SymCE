import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
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

def has_subgroup_of_order(G, m):
    try:
        m = int(m)
    except Exception:
        return False
        
    if m == 1:
        return True
        
    try:
        order_G = G.order()
    except Exception:
        return False
        
    if m == order_G:
        return True
    if order_G % m != 0:
        return False
        
    try:
        elements = list(G.elements)
    except Exception:
        return False
        
    valid_elements = []
    for g in elements:
        try:
            if m % g.order() == 0:
                valid_elements.append(g)
        except Exception:
            pass
            
    subgroups = set()
    queue = []
    
    for g in valid_elements:
        try:
            if g.is_Identity:
                continue
        except Exception:
            continue
            
        try:
            subg = PermutationGroup([g])
            order = subg.order()
            if m % order == 0:
                elems = frozenset(subg.elements)
                if elems not in subgroups:
                    subgroups.add(elems)
                    queue.append([g])
        except Exception:
            pass
            
    for elems in subgroups:
        if len(elems) == m:
            return True
            
    while queue:
        gens = queue.pop(0)
        try:
            current_subg = PermutationGroup(gens)
            current_elems = frozenset(current_subg.elements)
        except Exception:
            continue
            
        for g in valid_elements:
            if g in current_elems:
                continue
                
            new_gens = gens + [g]
            try:
                new_subg = PermutationGroup(new_gens)
                new_order = new_subg.order()
                
                if new_order == m:
                    return True
                    
                if m % new_order == 0:
                    new_elems = frozenset(new_subg.elements)
                    if new_elems not in subgroups:
                        subgroups.add(new_elems)
                        queue.append(new_gens)
            except Exception:
                pass
                
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, m, n = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and getattr(G, 'is_finite', True)
    except Exception:
        h1 = False
        
    try:
        m_val = int(m)
        n_val = int(n)
        h2 = (m_val > 0) and (n_val > 0) and (m == m_val) and (n == n_val) and (G.order() == m_val * n_val)
    except Exception:
        h2 = False
        
    try:
        h3 = math.gcd(int(m), int(n)) == 1
    except Exception:
        h3 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            neg_q = not has_subgroup_of_order(G, m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: m and n are positive integers such that the order of G is mn",
    "H_3: The greatest common divisor of m and n is 1",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3