import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

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

def to_hashable(x):
    try:
        hash(x)
        return x
    except TypeError:
        if hasattr(x, 'as_immutable'):
            return x.as_immutable()
        elif isinstance(x, list):
            return tuple(to_hashable(i) for i in x)
        elif isinstance(x, set):
            return frozenset(to_hashable(i) for i in x)
        return tuple(x)

def get_bounded_elements(G, max_elements=1000):
    if hasattr(G, 'generate'):
        els = []
        for i, x in enumerate(G.generate()):
            if i >= max_elements: break
            els.append(x)
        return els
    if hasattr(G, 'elements'):
        try:
            return list(G.elements)
        except Exception:
            pass
            
    gens = None
    if hasattr(G, 'generators'):
        gens = G.generators
    elif hasattr(G, 'gens'):
        gens = G.gens
    elif isinstance(G, (list, tuple, set)):
        gens = G
        
    if gens:
        elements = set(to_hashable(g) for g in gens)
        elements_list = list(gens)
        current_level = list(gens)
        
        try:
            g0 = current_level[0]
            g0_inv = ~g0 if hasattr(g0, '__invert__') else g0**-1
            identity = g0 * g0_inv
            if to_hashable(identity) not in elements:
                elements.add(to_hashable(identity))
                elements_list.append(identity)
        except Exception:
            pass
            
        while len(elements_list) < max_elements and current_level:
            next_level = []
            for g in current_level:
                for gen in gens:
                    try:
                        prod1 = g * gen
                        h1 = to_hashable(prod1)
                        if h1 not in elements:
                            elements.add(h1)
                            next_level.append(prod1)
                            elements_list.append(prod1)
                            
                        gen_inv = ~gen if hasattr(gen, '__invert__') else gen**-1
                        prod2 = g * gen_inv
                        h2 = to_hashable(prod2)
                        if h2 not in elements:
                            elements.add(h2)
                            next_level.append(prod2)
                            elements_list.append(prod2)
                    except Exception:
                        pass
                    if len(elements_list) >= max_elements:
                        break
                if len(elements_list) >= max_elements:
                    break
            current_level = next_level
        return elements_list
        
    return list(G)

def check_frobenius_complement(G, H):
    if hasattr(G, 'is_frobenius_complement'):
        return G.is_frobenius_complement(H)
    if hasattr(H, 'is_frobenius_complement_of'):
        return H.is_frobenius_complement_of(G)
        
    H_els = get_bounded_elements(H, max_elements=100)
    G_els = get_bounded_elements(G, max_elements=1000)
    
    if len(H_els) >= len(G_els) and len(G_els) < 1000:
        return False
    if len(H_els) <= 1:
        return False
        
    H_set = set(to_hashable(h) for h in H_els)
    
    for g in G_els:
        hg = to_hashable(g)
        if hg not in H_set:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
            gHg = set()
            for h in H_els:
                gHg.add(to_hashable(g * h * g_inv))
            if len(H_set.intersection(gHg)) != 1:
                return False
    return True

def check_conjugate(G, H, K):
    if hasattr(G, 'are_conjugate'):
        return G.are_conjugate(H, K)
        
    H_els = get_bounded_elements(H, max_elements=100)
    K_els = get_bounded_elements(K, max_elements=100)
    G_els = get_bounded_elements(G, max_elements=2000)
    
    H_set = set(to_hashable(h) for h in H_els)
    K_set = set(to_hashable(k) for k in K_els)
    
    if len(H_set) != len(K_set):
        return False
        
    for g in G_els:
        try:
            g_inv = ~g
        except Exception:
            g_inv = g**-1
        gHg = set()
        for h in H_els:
            gHg.add(to_hashable(g * h * g_inv))
        if gHg == K_set:
            return True
    return False

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        G, H, K = witness
    elif isinstance(witness, dict):
        G = witness['G']
        H = witness['H']
        K = witness['K']
    else:
        G = witness.G
        H = witness.H
        K = witness.K

    try:
        h1_H = check_frobenius_complement(G, H)
        h1_K = check_frobenius_complement(G, K)
        h1 = bool(h1_H and h1_K)
    except Exception:
        h1 = False

    try:
        conj = check_conjugate(G, H, K)
        neg_q = not conj
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H and K are Frobenius complements of G",
    "¬Q: H and K are not conjugate subgroups in G"
]
N_HYP = 1
NEG_Q_INDEX = 1