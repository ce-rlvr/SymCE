import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \\phi is a group homomorphism from G to H",
    "¬Q: The kernel \\ker(\\phi) is not a normal subgroup of G, or G/\\ker(\\phi) \\not\\cong \\phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(obj):
    if hasattr(obj, 'elements'):
        try:
            return list(obj.elements)
        except Exception:
            pass
    if hasattr(obj, 'generate') and callable(obj.generate):
        return list(obj.generate())
    elif isinstance(obj, (list, set, tuple)):
        return list(obj)
    return []

def apply_op(op, x, y):
    if op is not None:
        return op(x, y)
    return x * y

def apply_map(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def parse_witness(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        G_op = witness.get('G_op')
        H = witness.get('H')
        H_op = witness.get('H_op')
        phi = witness.get('phi')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            G, H, phi = witness
            G_op = None
            H_op = None
        elif len(witness) == 5:
            G, G_op, H, H_op, phi = witness
        else:
            raise ValueError("Invalid witness tuple length")
    else:
        raise ValueError("Witness must be dict or tuple")
    return G, G_op, H, H_op, phi

def is_group(G, G_op):
    if isinstance(G, PermutationGroup) and G_op is None:
        return True
    
    elements = get_elements(G)
    if not elements: 
        return False
    
    for x in elements:
        for y in elements:
            try:
                res = apply_op(G_op, x, y)
                if res not in elements:
                    return False
            except Exception:
                return False
                
    for x in elements:
        for y in elements:
            for z in elements:
                if apply_op(G_op, apply_op(G_op, x, y), z) != apply_op(G_op, x, apply_op(G_op, y, z)):
                    return False
                    
    identity = None
    for e in elements:
        if all(apply_op(G_op, e, x) == x and apply_op(G_op, x, e) == x for x in elements):
            identity = e
            break
            
    if identity is None:
        return False
        
    for x in elements:
        has_inv = False
        for y in elements:
            if apply_op(G_op, x, y) == identity and apply_op(G_op, y, x) == identity:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def is_homomorphism(G, G_op, H, H_op, phi):
    G_elems = get_elements(G)
    H_elems = get_elements(H)
    
    for x in G_elems:
        px = apply_map(phi, x)
        if px not in H_elems:
            return False
            
    for x in G_elems:
        for y in G_elems:
            xy = apply_op(G_op, x, y)
            pxy = apply_map(phi, xy)
            px = apply_map(phi, x)
            py = apply_map(phi, y)
            if pxy != apply_op(H_op, px, py):
                return False
                
    return True

def conclusion_holds(G, G_op, H, H_op, phi):
    G_elems = get_elements(G)
    H_elems = get_elements(H)
    
    e_H = None
    for e in H_elems:
        if all(apply_op(H_op, e, x) == x and apply_op(H_op, x, e) == x for x in H_elems):
            e_H = e
            break
            
    if e_H is None:
        return False
        
    ker = [x for x in G_elems if apply_map(phi, x) == e_H]
    
    if not ker:
        return False
        
    e_G = None
    for e in G_elems:
        if all(apply_op(G_op, e, x) == x and apply_op(G_op, x, e) == x for x in G_elems):
            e_G = e
            break
            
    if e_G not in ker:
        return False
        
    for x in ker:
        for y in ker:
            if apply_op(G_op, x, y) not in ker:
                return False
                
    for x in ker:
        has_inv = False
        for y in ker:
            if apply_op(G_op, x, y) == e_G and apply_op(G_op, y, x) == e_G:
                has_inv = True
                break
        if not has_inv:
            return False
            
    for g in G_elems:
        g_inv = None
        for y in G_elems:
            if apply_op(G_op, g, y) == e_G and apply_op(G_op, y, g) == e_G:
                g_inv = y
                break
        if g_inv is None:
            return False
            
        for k in ker:
            gk = apply_op(G_op, g, k)
            gkg_inv = apply_op(G_op, gk, g_inv)
            if gkg_inv not in ker:
                return False
                
    phi_G = []
    for x in G_elems:
        px = apply_map(phi, x)
        if px not in phi_G:
            phi_G.append(px)
            
    for x in phi_G:
        for y in phi_G:
            if apply_op(H_op, x, y) not in phi_G:
                return False
                
    e_phiG = None
    for e in phi_G:
        if all(apply_op(H_op, e, x) == x and apply_op(H_op, x, e) == x for x in phi_G):
            e_phiG = e
            break
            
    if e_phiG is None:
        return False
        
    for x in phi_G:
        has_inv = False
        for y in phi_G:
            if apply_op(H_op, x, y) == e_phiG and apply_op(H_op, y, x) == e_phiG:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def conditions(witness):
    try:
        G, G_op, H, H_op, phi = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_group(G, G_op)
    except Exception:
        h1 = False
        
    try:
        h2 = is_homomorphism(G, G_op, H, H_op, phi)
    except Exception:
        h2 = False
        
    try:
        q = conclusion_holds(G, G_op, H, H_op, phi)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]