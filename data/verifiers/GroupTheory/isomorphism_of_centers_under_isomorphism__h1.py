import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_center(grp):
    elements = list(grp.elements)
    center = set()
    for x in elements:
        if all(x * y == y * x for y in elements):
            center.add(x)
    return center

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False]
        
    if callable(phi):
        phi_func = phi
    else:
        phi_func = lambda x: phi[x]
        
    # H1: phi is a group isomorphism from G to H
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        H_elements_set = set(H_elements)
        
        h1 = True
        if len(G_elements) != len(H_elements):
            h1 = False
            
        if h1:
            mapped_values = set()
            for g in G_elements:
                try:
                    val = phi_func(g)
                    mapped_values.add(val)
                    if val not in H_elements_set:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
            if h1 and len(mapped_values) != len(H_elements):
                h1 = False
                
        if h1:
            for x in G_elements:
                for y in G_elements:
                    if phi_func(x * y) != phi_func(x) * phi_func(y):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # neg_Q: restriction of phi to Z(G) is NOT an isomorphism from Z(G) onto Z(H)
    try:
        Z_G = get_center(G)
        Z_H = get_center(H)
        
        is_iso = True
        phi_Z_G = set()
        for g in Z_G:
            try:
                val = phi_func(g)
                phi_Z_G.add(val)
            except Exception:
                is_iso = False
                break
                
        if is_iso and phi_Z_G != Z_H:
            is_iso = False
            
        if is_iso and len(phi_Z_G) != len(Z_G):
            is_iso = False
            
        if is_iso:
            for x in Z_G:
                for y in Z_G:
                    if phi_func(x * y) != phi_func(x) * phi_func(y):
                        is_iso = False
                        break
                if not is_iso:
                    break
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group isomorphism from G to H",
    "¬Q: The restriction of phi to Z(G) is not an isomorphism from Z(G) onto Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1