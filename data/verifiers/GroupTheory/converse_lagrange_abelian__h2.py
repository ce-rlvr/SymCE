import sympy
from sympy.combinatorics import PermutationGroup
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
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, m = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: m is a positive integer
    try:
        m_val = int(m)
        h2 = (m_val == m) and (m_val > 0)
    except Exception:
        h2 = False

    # H_3: m divides the order of G
    try:
        h3 = h1 and h2 and (G.order() % m_val == 0)
    except Exception:
        h3 = False

    # ¬Q: G does not contain a subgroup of order m
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            def has_subgroup_of_order(group, target_order):
                if target_order == 1:
                    return True
                if target_order == group.order():
                    return True
                
                try:
                    elements = list(group.elements)
                except AttributeError:
                    elements = list(group.generate_dimino())
                    
                N = len(elements)
                if N > 120:
                    raise ValueError("Group too large for exhaustive subgroup search")
                    
                id_el = group.identity
                el_to_idx = {e: i for i, e in enumerate(elements)}
                
                # Precompute multiplication table for fast closure
                mul_table = [[0] * N for _ in range(N)]
                for i in range(N):
                    for j in range(N):
                        mul_table[i][j] = el_to_idx[elements[i] * elements[j]]
                        
                subgroups = set()
                
                # Find all cyclic subgroups first
                for i in range(N):
                    H = {i}
                    curr = i
                    while curr != el_to_idx[id_el]:
                        curr = mul_table[curr][i]
                        H.add(curr)
                    subgroups.add(frozenset(H))
                    if len(H) == target_order:
                        return True
                        
                # Iteratively generate all subgroups by closure
                new_subgroups = set(subgroups)
                while new_subgroups:
                    added = set()
                    for H in new_subgroups:
                        for i in range(N):
                            if i in H:
                                continue
                            
                            closure = set(H)
                            queue = [i]
                            closure.add(i)
                            
                            while queue:
                                x = queue.pop(0)
                                for y in list(closure):
                                    xy = mul_table[x][y]
                                    if xy not in closure:
                                        closure.add(xy)
                                        queue.append(xy)
                                    yx = mul_table[y][x]
                                    if yx not in closure:
                                        closure.add(yx)
                                        queue.append(yx)
                                        
                            fs = frozenset(closure)
                            if len(fs) == target_order:
                                return True
                            if fs not in subgroups and fs not in added:
                                added.add(fs)
                                
                    subgroups.update(added)
                    new_subgroups = added
                    
                return False

            m_val = int(m)
            neg_q = not has_subgroup_of_order(G, m_val)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: m is a positive integer",
    "H_3: m divides the order of G",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3