import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return set(obj.elements)
    return set(obj)

def evaluate_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def get_identity(G):
    for g in G.elements:
        return g * ~g
    return None

def is_normal_subgroup(G, elements):
    try:
        G_elts = set(G.elements)
        elements = set(elements)
        if not elements.issubset(G_elts):
            return False
        
        identity = get_identity(G)
        if identity not in elements:
            return False
            
        for a in elements:
            for b in elements:
                if a * b not in elements:
                    return False
        for a in elements:
            if ~a not in elements:
                return False
        for g in G_elts:
            for n in elements:
                if g * n * ~g not in elements:
                    return False
        return True
    except Exception:
        return False

def get_normal_subgroups(G):
    try:
        if hasattr(G, 'normal_subgroups'):
            return [set(sg.elements) for sg in G.normal_subgroups()]
    except Exception:
        pass
    
    try:
        G_elts = list(G.elements)
        classes = []
        unseen = set(G_elts)
        while unseen:
            x = unseen.pop()
            c = set()
            for g in G_elts:
                c.add(g * x * ~g)
            classes.append(c)
            unseen -= c
            
        identity = get_identity(G)
        id_class = None
        for c in classes:
            if identity in c:
                id_class = c
                break
                
        other_classes = [c for c in classes if c != id_class]
        normal_sgs = []
        
        for r in range(len(other_classes) + 1):
            for combo in itertools.combinations(other_classes, r):
                elts = set(id_class)
                for c in combo:
                    elts.update(c)
                
                if len(G_elts) % len(elts) != 0:
                    continue
                
                if is_normal_subgroup(G, elts):
                    normal_sgs.append(elts)
        return normal_sgs
    except Exception:
        return []

def is_maximal_normal_subgroup(G, N_elts):
    try:
        N_set = set(N_elts)
        if not is_normal_subgroup(G, N_set):
            return False
        order_G = len(list(G.elements))
        if len(N_set) == order_G:
            return False
        
        for sg_set in get_normal_subgroups(G):
            if len(sg_set) > len(N_set) and len(sg_set) < order_G:
                if N_set.issubset(sg_set):
                    return False
        return True
    except Exception:
        return False

def get_ker(G, H, f):
    ker = set()
    id_H = get_identity(H)
    for g in G.elements:
        val = evaluate_f(f, g)
        if val == id_H:
            ker.add(g)
    return ker

def get_image(N_elts, f):
    img = set()
    for n in N_elts:
        val = evaluate_f(f, n)
        img.add(val)
    return img

def conditions(witness):
    try:
        G, H, N, f = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a maximal normal subgroup of G
    try:
        N_elts = get_elements(N)
        h2 = is_maximal_normal_subgroup(G, N_elts)
    except Exception:
        h2 = False
        
    # H3: ker(f) is a subset of N
    try:
        N_elts = get_elements(N)
        ker = get_ker(G, H, f)
        h3 = ker.issubset(N_elts)
    except Exception:
        h3 = False
        
    # neg_Q: f(N) is not a maximal normal subgroup of H
    try:
        N_elts = get_elements(N)
        img = get_image(N_elts, f)
        neg_q = not is_maximal_normal_subgroup(H, img)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: N is a maximal normal subgroup of G",
    "H_3: ker(f) is a subset of N",
    "¬Q: f(N) is not a maximal normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3