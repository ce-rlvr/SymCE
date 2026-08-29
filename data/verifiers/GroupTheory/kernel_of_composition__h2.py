import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def get_witness_value(witness, key):
    if isinstance(witness, dict):
        return witness.get(key)
    return getattr(witness, key, None)

def get_map_value(mapping, key):
    if isinstance(mapping, dict):
        return mapping[key]
    else:
        return mapping(key)

def check_H1(witness):
    G = get_witness_value(witness, 'G')
    H = get_witness_value(witness, 'H')
    K = get_witness_value(witness, 'K')
    
    if G is None or H is None or K is None:
        return False
        
    for grp in (G, H, K):
        if not hasattr(grp, 'elements') or not hasattr(grp, 'identity'):
            return False
    return True

def check_H2(witness):
    H = get_witness_value(witness, 'H')
    K = get_witness_value(witness, 'K')
    g = get_witness_value(witness, 'g')
    
    if H is None or K is None or g is None:
        return False
        
    H_els = list(H.elements)
    K_els = list(K.elements)
    
    for x in H_els:
        try:
            gx = get_map_value(g, x)
        except Exception:
            return False
        if gx not in K_els: 
            return False
            
    for x in H_els:
        for y in H_els:
            try:
                gx = get_map_value(g, x)
                gy = get_map_value(g, y)
                gxy = get_map_value(g, x * y)
                if gxy != gx * gy: 
                    return False
            except Exception:
                return False
                
    return True

def check_neg_Q(witness):
    G = get_witness_value(witness, 'G')
    H = get_witness_value(witness, 'H')
    K = get_witness_value(witness, 'K')
    f = get_witness_value(witness, 'f')
    g = get_witness_value(witness, 'g')
    
    if any(v is None for v in (G, H, K, f, g)):
        return False
        
    G_els = list(G.elements)
    H_els = list(H.elements)
    
    for x in G_els:
        try:
            fx = get_map_value(f, x)
        except Exception:
            return False
        if fx not in H_els: 
            return False
            
    e_H = H.identity
    ker_f = set()
    for x in G_els:
        try:
            if get_map_value(f, x) == e_H:
                ker_f.add(x)
        except Exception:
            return False
            
    e_K = K.identity
    ker_gf = set()
    for x in G_els:
        try:
            if get_map_value(g, get_map_value(f, x)) == e_K:
                ker_gf.add(x)
        except Exception:
            return False
            
    is_subset = ker_f.issubset(ker_gf)
    
    e_G = G.identity
    if e_G not in ker_f:
        is_subgroup = False
    else:
        is_subgroup = True
        for x in ker_f:
            for y in ker_f:
                try:
                    if (x * y) not in ker_f:
                        is_subgroup = False
                        break
                except Exception:
                    is_subgroup = False
                    break
            if not is_subgroup:
                break
            try:
                if (x**-1) not in ker_f:
                    is_subgroup = False
                    break
            except Exception:
                is_subgroup = False
                break
                
    conclusion = is_subset and is_subgroup
    return not conclusion

def conditions(witness) -> list[bool]:
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, H, and K are groups",
    "H_2: g: H \\to K is a group homomorphism",
    "¬Q: The kernel of f is not a subgroup of the kernel of g \\circ f"
]

N_HYP = 2
NEG_Q_INDEX = 2