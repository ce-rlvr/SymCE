import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def is_supersolvable(G):
    # Fast paths for known supersolvable/non-supersolvable classes
    is_nil = getattr(G, 'is_nilpotent', None)
    if callable(is_nil):
        is_nil = is_nil()
    if is_nil:
        return True
        
    is_ab = getattr(G, 'is_abelian', None)
    if callable(is_ab):
        is_ab = is_ab()
    if is_ab:
        return True
        
    is_solv = getattr(G, 'is_solvable', None)
    if callable(is_solv):
        is_solv = is_solv()
    if is_solv is False:
        return False

    order_attr = G.order
    if callable(order_attr):
        order = order_attr()
    else:
        order = order_attr
    if order == 1:
        return True
        
    if hasattr(G, 'elements'):
        elements = list(G.elements)
    else:
        elements = list(G.generate())
        
    # Find the identity element robustly
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    if id_elem is None:
        return False

    # Compute conjugacy classes
    classes = []
    seen = set()
    for g in elements:
        if g in seen:
            continue
        c = set()
        for h in elements:
            try:
                h_inv = h**-1
            except Exception:
                h_inv = ~h
            c.add(h_inv * g * h)
        classes.append(list(c))
        seen.update(c)
        
    other_classes = [c for c in classes if id_elem not in c]
    elem_to_class = {}
    for i, c in enumerate(other_classes):
        for g in c:
            elem_to_class[g] = i
            
    def get_closure(base_set):
        current = set(base_set)
        while True:
            new_elements = set()
            current_list = list(current)
            for x in current_list:
                for y in current_list:
                    xy = x * y
                    if xy not in current:
                        new_elements.add(xy)
            if not new_elements:
                break
            for x in new_elements:
                if x != id_elem:
                    current.update(other_classes[elem_to_class[x]])
        return frozenset(current)

    # Find all normal subgroups by exploring combinations of conjugacy classes
    known = set()
    queue = [frozenset([id_elem])]
    visited = set(queue)
    
    while queue:
        current = queue.pop(0)
        known.add(current)
        
        for c in other_classes:
            if c[0] not in current:
                new_base = set(current)
                new_base.update(c)
                closed = get_closure(new_base)
                if closed not in visited:
                    visited.add(closed)
                    queue.append(closed)
                    
    ns_list = sorted(list(known), key=len)
    
    # BFS to find a path from {1} to G where each step has prime index
    queue_bfs = [ns_list[0]]
    visited_bfs = set([ns_list[0]])
    target = ns_list[-1]
    
    if ns_list[0] == target:
        return True
        
    while queue_bfs:
        current = queue_bfs.pop(0)
        
        for candidate in ns_list:
            if len(candidate) <= len(current):
                continue
            if candidate in visited_bfs:
                continue
                
            ratio = len(candidate) // len(current)
            if len(candidate) % len(current) == 0 and isprime(ratio):
                if current.issubset(candidate):
                    if candidate == target:
                        return True
                    visited_bfs.add(candidate)
                    queue_bfs.append(candidate)
                    
    return False

def conditions(witness):
    # H1: G is a group
    try:
        h1 = hasattr(witness, 'generators') or hasattr(witness, 'generate') or hasattr(witness, 'elements')
    except Exception:
        h1 = False

    # H2: G is a finite group
    try:
        if hasattr(witness, 'order'):
            order_attr = witness.order
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
            h2 = order < float('inf')
        elif hasattr(witness, 'is_finite'):
            is_fin = witness.is_finite
            if callable(is_fin):
                h2 = bool(is_fin())
            else:
                h2 = bool(is_fin)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G is NOT a supersolvable group
    try:
        if not h2:
            neg_q = False
        else:
            neg_q = not is_supersolvable(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is a finite group",
    "¬Q: G is not a supersolvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2