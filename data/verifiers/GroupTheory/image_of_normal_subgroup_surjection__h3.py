import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'generate') and callable(group.generate):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def get_inv(a):
    try:
        return ~a
    except Exception:
        pass
    try:
        return a**-1
    except Exception:
        pass
    try:
        return a.inv()
    except Exception:
        pass
    return None

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    if hasattr(group, 'generators') and len(group.generators) > 0:
        g = group.generators[0]
        return g * get_inv(g)
    return None

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        N = witness.get('N')
        phi = witness.get('phi')
    else:
        try:
            G, H, N, phi = witness
        except Exception:
            return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'generators')
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = hasattr(H, 'generators')
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = True
        if not hasattr(N, 'generators'):
            h3 = False
        else:
            for gen in N.generators:
                if gen not in G:
                    h3 = False
                    break
            if h3:
                for g in G.generators:
                    g_inv = get_inv(g)
                    for n in N.generators:
                        if (g * n * g_inv) not in N:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: The image phi(N) is not a normal subgroup of H
    try:
        image_N = set()
        N_elements = get_elements(N)
        for n in N_elements:
            if isinstance(phi, dict):
                image_N.add(phi[n])
            elif callable(phi):
                image_N.add(phi(n))
            else:
                image_N.add(phi[n])
        
        is_subgroup = True
        id_H = get_identity(H)
        if id_H is not None and id_H not in image_N:
            is_subgroup = False
        elif id_H is None and not image_N:
            is_subgroup = False
        
        if is_subgroup:
            for x in image_N:
                if x not in H:
                    is_subgroup = False
                    break
            
            if is_subgroup:
                for a in image_N:
                    a_inv = get_inv(a)
                    if a_inv not in image_N:
                        is_subgroup = False
                        break
                    for b in image_N:
                        if a * b not in image_N:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                    
        is_normal = is_subgroup
        if is_subgroup:
            H_elements = get_elements(H)
            for h in H_elements:
                h_inv = get_inv(h)
                for x in image_N:
                    if (h * x * h_inv) not in image_N:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: N is a normal subgroup of G",
    "¬Q: The image phi(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3