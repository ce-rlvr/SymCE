import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup
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

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    if G.generators:
        g = G.generators[0]
        return g * ~g
    try:
        elements = list(G.elements)
    except AttributeError:
        elements = list(G.generate_dimino())
    for g in elements:
        if g * g == g:
            return g
    return None

def contains(group, elem):
    if hasattr(group, 'contains'):
        return group.contains(elem)
    return elem in group

def check_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        return H.is_subgroup(G)
    return all(contains(G, g) for g in H.generators)

def check_normal(H, G):
    if hasattr(H, 'is_normal'):
        return H.is_normal(G)
    for g in G.generators:
        g_inv = ~g
        for h in H.generators:
            if not contains(H, g * h * g_inv):
                return False
    return True

def generate_group(generators, allowed, max_size):
    closure = set(generators)
    queue = list(generators)
    while queue:
        x = queue.pop()
        for y in generators:
            for new_elem in (x * y, y * x):
                if new_elem not in closure:
                    if new_elem not in allowed or len(closure) >= max_size:
                        return None
                    closure.add(new_elem)
                    queue.append(new_elem)
    return closure

def has_complement_subgroup(G, N, index):
    try:
        elements = list(G.elements)
    except AttributeError:
        elements = list(G.generate_dimino())
        
    identity = get_identity(G)
    allowed = set(g for g in elements if not contains(N, g) or g == identity)
    
    if index == 1:
        return True
        
    valid_elements = []
    for g in allowed:
        if g == identity:
            continue
        if index % g.order() != 0:
            continue
        cg = generate_group([g], allowed, index)
        if cg is not None:
            valid_elements.append(g)
            
    subgroups = [frozenset([identity])]
    
    for g in valid_elements:
        new_subgroups = []
        for H in subgroups:
            if g in H:
                continue
            generators = list(H) + [g]
            closure = generate_group(generators, allowed, index)
            if closure is not None:
                if len(closure) == index:
                    return True
                fs = frozenset(closure)
                if fs not in subgroups and fs not in new_subgroups:
                    new_subgroups.append(fs)
        subgroups.extend(new_subgroups)
        
    return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(N, PermutationGroup) and check_subgroup(N, G) and check_normal(N, G)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            index = G.order() // N.order()
            has_complement = has_complement_subgroup(G, N, index)
            neg_q = not has_complement
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: no complement subgroup H exists"
]
N_HYP = 2
NEG_Q_INDEX = 2