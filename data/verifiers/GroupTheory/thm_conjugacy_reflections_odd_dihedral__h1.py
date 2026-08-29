import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is the dihedral group of order 2n",
    "H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G",
    "¬Q: R does not constitute exactly one conjugacy class in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(obj):
    if callable(obj.order):
        return obj.order()
    return obj.order

def get_elements(G):
    if callable(G.elements):
        return list(G.elements())
    return list(G.elements)

def is_dihedral(G):
    if not hasattr(G, 'order') or not hasattr(G, 'elements'): 
        return False
    order = get_order(G)
    if order % 2 != 0: 
        return False
    n = order // 2
    if n < 1: 
        return False
    
    elements = get_elements(G)
    if n == 1:
        return order == 2
    if n == 2:
        return order == 4 and all(get_order(g) in (1, 2) for g in elements)
    
    rotations = [g for g in elements if get_order(g) == n]
    reflections = [g for g in elements if get_order(g) == 2]
    for r in rotations:
        for s in reflections:
            if s * r * s == r ** -1:
                return True
    return False

def conditions(witness) -> list[bool]:
    try:
        G, R_iter = witness
        R = list(R_iter)
    except Exception:
        return [False, False, False]
    
    # H_1: G is the dihedral group of order 2n
    try:
        h1 = is_dihedral(G)
    except Exception:
        h1 = False
        
    # H_2: R is the set of all reflections in G
    try:
        h2 = False
        if h1:
            n = get_order(G) // 2
            elements = get_elements(G)
            possible_C = []
            if n == 1:
                possible_C.append({g for g in elements if get_order(g) == 1})
            else:
                for g in elements:
                    if get_order(g) == n:
                        C = set()
                        curr = g
                        while curr not in C:
                            C.add(curr)
                            curr = curr * g
                        if C not in possible_C:
                            possible_C.append(C)
            
            for C in possible_C:
                expected_R = {g for g in elements if get_order(g) == 2 and g not in C}
                if set(R) == expected_R:
                    h2 = True
                    break
    except Exception:
        h2 = False
        
    # ¬Q: R does not constitute exactly one conjugacy class in G
    try:
        neg_q = False
        if hasattr(G, 'elements') and hasattr(R, '__iter__'):
            R_set = set(R)
            if not R_set:
                neg_q = True
            else:
                r = list(R_set)[0]
                elements = get_elements(G)
                if r in elements:
                    conj_class = {g * r * (g ** -1) for g in elements}
                    if conj_class != R_set:
                        neg_q = True
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]