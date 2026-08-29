import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: m is a positive integer",
    "H_3: m divides the order of G",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3

def has_subgroup_of_order(G, m):
    if m == 1:
        return True
    try:
        order = G.order()
    except Exception:
        return False
        
    if m == order:
        return True
    if order % m != 0:
        return False
        
    # Finite abelian groups always satisfy the converse of Lagrange's theorem
    if getattr(G, 'is_abelian', False):
        return True

    try:
        elements = list(G.elements)
        id_el = G.identity
    except Exception:
        return False
        
    # Any element in a subgroup of order m must have an order dividing m
    valid_elements = [e for e in elements if m % e.order() == 0]
    
    # BFS to find if any subgroup of order m exists
    known_subgroups = {frozenset([id_el])}
    queue = [frozenset([id_el])]
    
    while queue:
        curr = queue.pop(0)
        for e in valid_elements:
            if e not in curr:
                # Compute the closure of the current subgroup with the new element
                closure = set(curr)
                inner_queue = [e]
                closure.add(e)
                
                exceeded = False
                while inner_queue:
                    c = inner_queue.pop(0)
                    new_items = []
                    for g in list(closure):
                        p1 = c * g
                        if p1 not in closure:
                            closure.add(p1)
                            new_items.append(p1)
                            if len(closure) > m:
                                exceeded = True
                                break
                        p2 = g * c
                        if p2 not in closure:
                            closure.add(p2)
                            new_items.append(p2)
                            if len(closure) > m:
                                exceeded = True
                                break
                    if exceeded:
                        break
                    inner_queue.extend(new_items)
                
                if exceeded:
                    continue
                    
                if len(closure) == m:
                    return True
                    
                if len(closure) < m:
                    fs = frozenset(closure)
                    if fs not in known_subgroups:
                        known_subgroups.add(fs)
                        queue.append(fs)
                        
    return False

def conditions(witness) -> list[bool]:
    try:
        G, m = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is an abelian group
    try:
        h1_ok = bool(G.is_abelian)
    except Exception:
        h1_ok = False
        
    # H_2: m is a positive integer
    try:
        h2_ok = (int(m) == m) and (m > 0)
    except Exception:
        h2_ok = False
        
    # H_3: m divides the order of G
    try:
        h3_ok = (G.order() % m == 0)
    except Exception:
        h3_ok = False
        
    # ¬Q: G does not contain a subgroup of order m
    try:
        has_sub = has_subgroup_of_order(G, m)
        neg_q_ok = not has_sub
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]