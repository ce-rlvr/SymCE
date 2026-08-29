import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def get_identity(group, elements):
    if hasattr(group, 'identity'):
        return group.identity
    for e in elements:
        is_id = True
        for x in elements:
            if e * x != x or x * e != x:
                is_id = False
                break
        if is_id:
            return e
    return None

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        K = witness['K']
    except Exception:
        return [False, False, False]
        
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(f, dict):
            f_map = f
        elif isinstance(f, (list, tuple)):
            f_map = dict(f)
        elif callable(f):
            f_map = {g: f(g) for g in G_elems}
        else:
            f_map = None
    except Exception:
        f_map = None

    # H1: f is a group homomorphism from G to H
    h1 = False
    try:
        if f_map is not None and set(f_map.keys()) == set(G_elems) and all(v in H_elems for v in f_map.values()):
            is_homo = True
            for x in G_elems:
                for y in G_elems:
                    if f_map[x * y] != f_map[x] * f_map[y]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            h1 = is_homo
    except Exception:
        h1 = False

    # H2: K is a subgroup of H
    h2 = False
    try:
        K_set = set(K)
        if K_set.issubset(set(H_elems)) and len(K_set) > 0:
            is_subgroup = True
            for x in K_set:
                for y in K_set:
                    if x * y not in K_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            if is_subgroup:
                id_H = get_identity(H, H_elems)
                if id_H not in K_set:
                    is_subgroup = False
                else:
                    for x in K_set:
                        has_inv = False
                        for y in K_set:
                            if x * y == id_H and y * x == id_H:
                                has_inv = True
                                break
                        if not has_inv:
                            is_subgroup = False
                            break
            h2 = is_subgroup
    except Exception:
        h2 = False

    # Conclusion: preimage is a subgroup of G containing ker(f)
    neg_q = False
    try:
        if f_map is not None:
            K_set = set(K)
            preimage = {g for g in G_elems if f_map[g] in K_set}
            
            is_preimage_subgroup = True
            if len(preimage) == 0:
                is_preimage_subgroup = False
            else:
                for x in preimage:
                    for y in preimage:
                        if x * y not in preimage:
                            is_preimage_subgroup = False
                            break
                    if not is_preimage_subgroup:
                        break
                
                if is_preimage_subgroup:
                    id_G = get_identity(G, G_elems)
                    if id_G not in preimage:
                        is_preimage_subgroup = False
                    else:
                        for x in preimage:
                            has_inv = False
                            for y in preimage:
                                if x * y == id_G and y * x == id_G:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_preimage_subgroup = False
                                break
                                
            id_H = get_identity(H, H_elems)
            kernel = {g for g in G_elems if f_map[g] == id_H}
            contains_kernel = kernel.issubset(preimage)
            
            q = is_preimage_subgroup and contains_kernel
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: K is a subgroup of H",
    "¬Q: The preimage f^{-1}(K) is not a subgroup of G or does not contain the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2