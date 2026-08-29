import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'generate'):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def get_identity(elements):
    for e in elements:
        if e * e == e:
            return e
    return None

def get_inverse(x, elements, identity):
    try:
        return x**-1
    except Exception:
        try:
            return ~x
        except Exception:
            for y in elements:
                if x * y == identity and y * x == identity:
                    return y
            return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            N = witness['N']
        else:
            G, H, f, N = witness
    except Exception:
        return [False, False, False, False]

    if isinstance(f, dict):
        f_val = lambda x: f.get(x, None)
    else:
        f_val = f

    try:
        G_elements = get_elements(G)
        H_elements = get_elements(H)
    except Exception:
        return [False, False, False, False]

    # H_1: f is a group homomorphism from G to H
    try:
        h1 = True
        for g in G_elements:
            val = f_val(g)
            if val is None or val not in H_elements:
                h1 = False
                break
                
        if h1:
            for g1 in G_elements:
                for g2 in G_elements:
                    if f_val(g1 * g2) != f_val(g1) * f_val(g2):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: f is surjective
    try:
        image_f = []
        for g in G_elements:
            val = f_val(g)
            if val not in image_f:
                image_f.append(val)
        
        h2 = True
        for h in H_elements:
            if h not in image_f:
                h2 = False
                break
        if h2:
            for img in image_f:
                if img not in H_elements:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        N_elements = get_elements(N)
        
        h3 = True
        for n in N_elements:
            if n not in G_elements:
                h3 = False
                break
                
        if h3:
            id_G = get_identity(G_elements)
            if id_G not in N_elements:
                h3 = False
            else:
                for n1 in N_elements:
                    inv_n1 = get_inverse(n1, G_elements, id_G)
                    if inv_n1 not in N_elements:
                        h3 = False
                        break
                    for n2 in N_elements:
                        if n1 * n2 not in N_elements:
                            h3 = False
                            break
                    if not h3:
                        break
                        
            if h3:
                for n in N_elements:
                    for g in G_elements:
                        inv_g = get_inverse(g, G_elements, id_G)
                        if g * n * inv_g not in N_elements:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: f(N) is NOT a normal subgroup of H
    try:
        f_N = []
        for n in N_elements:
            val = f_val(n)
            if val not in f_N:
                f_N.append(val)
                
        id_H = get_identity(H_elements)
        
        is_normal = True
        for y in f_N:
            for h in H_elements:
                inv_h = get_inverse(h, H_elements, id_H)
                if h * y * inv_h not in f_N:
                    is_normal = False
                    break
            if not is_normal:
                break
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: f is surjective",
    "H_3: N is a normal subgroup of G",
    "¬Q: f(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3