import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_order(grp):
    return grp.order() if callable(grp.order) else grp.order

def conditions(witness):
    try:
        G, H, f, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'order') and hasattr(H, 'order')
    except Exception:
        h1 = False
        
    # H_2: f is a surjective group homomorphism
    try:
        elements_G = list(G.elements)
        elements_H = list(H.elements)
        
        if isinstance(f, dict):
            mapping = f
        else:
            mapping = {g: f(g) for g in elements_G}
            
        is_hom = True
        for g1 in elements_G:
            for g2 in elements_G:
                if mapping[g1 * g2] != mapping[g1] * mapping[g2]:
                    is_hom = False
                    break
            if not is_hom:
                break
                
        image = set(mapping[g] for g in elements_G)
        is_surj = image == set(elements_H)
        
        h2 = is_hom and is_surj
    except Exception:
        h2 = False
        
    # H_3: The index of N in G is finite
    try:
        if hasattr(N, 'elements'):
            elements_N = list(N.elements)
        else:
            elements_N = list(N)
            
        is_subgroup = all(n in elements_G for n in elements_N)
        is_closed = len(elements_N) > 0
        for n1 in elements_N:
            for n2 in elements_N:
                if n1 * n2 not in elements_N:
                    is_closed = False
                    break
            if not is_closed:
                break
        
        order_G = _get_order(G)
        order_N = len(elements_N)
        h3 = is_subgroup and is_closed and (order_G % order_N == 0)
    except Exception:
        h3 = False
        
    # not Q: The index of f(N) in H does not divide the index of N in G
    try:
        image_N = set(mapping[n] for n in elements_N)
        len_image_N = len(image_N)
        
        order_G = _get_order(G)
        order_H = _get_order(H)
        
        index_G_N = order_G // order_N
        index_H_fN = order_H // len_image_N
        
        neg_q = (index_G_N % index_H_fN) != 0
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism",
    "H_3: The index of N in G is finite",
    "not Q: The index of f(N) in H does not divide the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3