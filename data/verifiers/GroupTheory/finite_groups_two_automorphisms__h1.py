import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
Z = sympy.S.Integers
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def count_automorphisms(G):
    if G == sympy.S.Integers or str(G) in ("Z", "Z_infty", "Z_inf", "Integers"):
        return 2
    
    if type(G).__name__ == 'FreeGroup':
        if len(G.generators) == 1:
            return 2
        else:
            return -1
            
    if type(G).__name__ == 'FpGroup':
        if len(G.generators) == 1 and len(G.relators) == 0:
            return 2
        try:
            if G.order() == sympy.oo:
                return -1
        except Exception:
            pass

    if not hasattr(G, 'elements'):
        return -1
        
    try:
        elements = list(G.elements)
    except Exception:
        return -1
        
    n = len(elements)
    if n == 1:
        return 1
        
    gens = getattr(G, 'generators', None)
    if not gens:
        return -1
        
    identity = None
    for e in elements:
        if e.order() == 1:
            identity = e
            break
    if identity is None:
        return -1
        
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    orders = [e.order() for e in elements]
    
    possible_images = []
    for g in gens:
        g_order = g.order()
        images = [i for i, e in enumerate(elements) if orders[i] == g_order]
        possible_images.append(images)
        
    aut_count = 0
    
    for img_tuple in itertools.product(*possible_images):
        full_map = {elem_to_idx[identity]: elem_to_idx[identity]}
        queue = [elem_to_idx[identity]]
        valid = True
        
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_img = full_map[curr]
            
            for i, g in enumerate(gens):
                next_elem = elements[curr] * g
                next_idx = elem_to_idx[next_elem]
                
                next_img_elem = elements[curr_img] * elements[img_tuple[i]]
                next_img_idx = elem_to_idx[next_img_elem]
                
                if next_idx in full_map:
                    if full_map[next_idx] != next_img_idx:
                        valid = False
                        break
                else:
                    full_map[next_idx] = next_img_idx
                    queue.append(next_idx)
            if not valid:
                break
                
        if valid and len(full_map) == n and len(set(full_map.values())) == n:
            aut_count += 1
            
    return aut_count

def is_isomorphic_to_Z3_Z4_Z6(G):
    if G == sympy.S.Integers or str(G) in ("Z", "Z_infty", "Z_inf", "Integers"):
        return False
        
    if type(G).__name__ == 'FreeGroup':
        return False
    if type(G).__name__ == 'FpGroup':
        try:
            if G.order() == sympy.oo:
                return False
        except Exception:
            pass
            
    if not hasattr(G, 'order'):
        return False
        
    try:
        order = G.order()
    except Exception:
        return False
        
    if order not in (3, 4, 6):
        return False
        
    if order == 3:
        return True
    if order == 4:
        try:
            return any(g.order() == 4 for g in G.elements)
        except Exception:
            return False
    if order == 6:
        try:
            return getattr(G, 'is_abelian', False)
        except Exception:
            return False
            
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = (count_automorphisms(witness) == 2)
    except Exception:
        h1 = False
        
    try:
        q = is_isomorphic_to_Z3_Z4_Z6(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The automorphism group of G has exactly two elements",
    "¬Q: G is not isomorphic to Z_3, Z_4, or Z_6"
]

N_HYP = 1
NEG_Q_INDEX = 1