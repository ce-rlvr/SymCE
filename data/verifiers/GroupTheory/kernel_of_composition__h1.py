import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        els = group.elements
        if callable(els):
            return list(els())
        return list(els)
    elif isinstance(group, (list, tuple, set)):
        return list(group)
    else:
        raise TypeError("Cannot get elements from group")

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    elements = get_elements(group)
    for e in elements:
        if all(e * x == x and x * e == x for x in elements):
            return e
    raise ValueError("No identity found")

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['H'], witness['K'], witness['f'], witness['g']
    elif isinstance(witness, (list, tuple)) and len(witness) == 5:
        return witness[0], witness[1], witness[2], witness[3], witness[4]
    else:
        raise ValueError("Witness must be a dict or a 5-tuple")

def eval_map(m, x):
    if isinstance(m, dict):
        return m[x]
    return m(x)

def conditions(witness) -> list[bool]:
    try:
        G, H, K, f, g = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: f is a group homomorphism from G to H
    h1_ok = False
    try:
        G_els = get_elements(G)
        H_els = get_elements(H)
        h1_ok = True
        for a in G_els:
            if eval_map(f, a) not in H_els:
                h1_ok = False
                break
        if h1_ok:
            for a in G_els:
                for b in G_els:
                    if eval_map(f, a * b) != eval_map(f, a) * eval_map(f, b):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: g is a group homomorphism from H to K
    h2_ok = False
    try:
        H_els = get_elements(H)
        K_els = get_elements(K)
        h2_ok = True
        for a in H_els:
            if eval_map(g, a) not in K_els:
                h2_ok = False
                break
        if h2_ok:
            for a in H_els:
                for b in H_els:
                    if eval_map(g, a * b) != eval_map(g, a) * eval_map(g, b):
                        h2_ok = False
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False

    # neg_Q: The kernel of f is NOT a subgroup of the kernel of g \circ f
    neg_q_ok = False
    try:
        G_els = get_elements(G)
        id_G = get_identity(G)
        id_H = get_identity(H)
        id_K = get_identity(K)
        
        ker_f = []
        for x in G_els:
            if eval_map(f, x) == id_H:
                ker_f.append(x)
                
        ker_gf = []
        for x in G_els:
            if eval_map(g, eval_map(f, x)) == id_K:
                ker_gf.append(x)
                
        is_subset = all(x in ker_gf for x in ker_f)
        
        is_group = True
        if id_G not in ker_f:
            is_group = False
        else:
            for a in ker_f:
                has_inv = False
                for b in ker_f:
                    if a * b == id_G and b * a == id_G:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                for b in ker_f:
                    if (a * b) not in ker_f:
                        is_group = False
                        break
                if not is_group:
                    break
                    
        is_gf_group = True
        if id_G not in ker_gf:
            is_gf_group = False
        else:
            for a in ker_gf:
                has_inv = False
                for b in ker_gf:
                    if a * b == id_G and b * a == id_G:
                        has_inv = True
                        break
                if not has_inv:
                    is_gf_group = False
                    break
                for b in ker_gf:
                    if (a * b) not in ker_gf:
                        is_gf_group = False
                        break
                if not is_gf_group:
                    break
                    
        is_subgroup = is_subset and is_group and is_gf_group
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: g is a group homomorphism from H to K",
    "¬Q: The kernel of f is not a subgroup of the kernel of g \\circ f"
]

N_HYP = 2
NEG_Q_INDEX = 2