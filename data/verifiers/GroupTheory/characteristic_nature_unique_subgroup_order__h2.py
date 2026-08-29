import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def get_all_subgroups(G):
    elements = list(G.generate())
    
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    def closure(gens):
        if not gens:
            return frozenset([identity]) if identity else frozenset()
        s = set(gens)
        q = list(gens)
        while q:
            x = q.pop()
            for y in list(s):
                xy = x * y
                if xy not in s:
                    s.add(xy)
                    q.append(xy)
                yx = y * x
                if yx not in s:
                    s.add(yx)
                    q.append(yx)
        return frozenset(s)

    cyclic = set()
    if identity:
        cyclic.add(frozenset([identity]))
    for g in elements:
        cyclic.add(closure([g]))
    
    subgroups_set = set(cyclic)
    current_level = list(cyclic)
    
    while True:
        new_level = set()
        for A in current_level:
            for B in cyclic:
                if not B.issubset(A):
                    C = closure(A | B)
                    if C not in subgroups_set:
                        new_level.add(C)
                        subgroups_set.add(C)
        if not new_level:
            break
        current_level = list(new_level)
        
    return subgroups_set

def get_automorphisms(G):
    gens = G.generators
    G_elems = list(G.generate())
    
    identity = None
    for e in G_elems:
        if e * e == e:
            identity = e
            break
            
    if identity is None:
        return []

    def closure(generators):
        if not generators:
            return {identity}
        s = set(generators)
        q = list(generators)
        while q:
            x = q.pop()
            for y in list(s):
                xy = x * y
                if xy not in s:
                    s.add(xy)
                    q.append(xy)
                yx = y * x
                if yx not in s:
                    s.add(yx)
                    q.append(yx)
        return s

    automorphisms = []
    
    for target_gens in itertools.product(G_elems, repeat=len(gens)):
        if len(closure(target_gens)) != len(G_elems):
            continue
            
        mapping = {}
        valid = True
        
        q = [ (identity, identity) ]
        mapping[identity] = identity
        
        for g, tg in zip(gens, target_gens):
            if g in mapping:
                if mapping[g] != tg:
                    valid = False
                    break
            else:
                mapping[g] = tg
                q.append((g, tg))
                
        if not valid:
            continue
            
        head = 0
        while head < len(q):
            x, tx = q[head]
            head += 1
            
            for g, tg in zip(gens, target_gens):
                y = x * g
                ty = tx * tg
                if y in mapping:
                    if mapping[y] != ty:
                        valid = False
                        break
                else:
                    mapping[y] = ty
                    q.append((y, ty))
            if not valid:
                break
                
        if valid and len(mapping) == len(G_elems):
            automorphisms.append(mapping)
            
    return automorphisms

def is_subgroup(G, H_elems):
    if not H_elems:
        return False
    G_elems = frozenset(G.generate())
    if not H_elems.issubset(G_elems):
        return False
    for x in H_elems:
        for y in H_elems:
            if x * y not in H_elems:
                return False
    return True

def is_characteristic(G, H_elems):
    if not is_subgroup(G, H_elems):
        return False
        
    autos = get_automorphisms(G)
    for mapping in autos:
        mapped_H = set(mapping[h] for h in H_elems)
        if mapped_H != set(H_elems):
            return False
            
    return True

def check_cond1(G):
    try:
        if hasattr(G, 'order'):
            return G.order() < float('inf')
        if hasattr(G, 'generate'):
            return len(list(G.generate())) > 0
    except Exception:
        pass
    return False

def check_cond2(G, H):
    try:
        h_order = H.order()
    except AttributeError:
        try:
            h_order = len(list(H.generate())) if hasattr(H, 'generate') else len(H)
        except Exception:
            return False
            
    if h_order == 0:
        return False
        
    try:
        g_order = G.order()
    except AttributeError:
        g_order = len(list(G.generate()))
        
    if g_order % h_order != 0:
        return True
        
    subgroups = get_all_subgroups(G)
    
    try:
        if hasattr(H, 'generate'):
            H_elems = frozenset(H.generate())
        else:
            H_elems = frozenset(H)
    except Exception:
        H_elems = None

    other_count = 0
    for S in subgroups:
        if len(S) == h_order:
            if H_elems is not None and S == H_elems:
                continue
            other_count += 1
            
    return other_count == 0

def check_neg_q(G, H):
    try:
        if hasattr(H, 'generate'):
            H_elems = frozenset(H.generate())
        else:
            H_elems = frozenset(H)
    except Exception:
        return True
        
    return not is_characteristic(G, H_elems)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        else:
            G = witness.G
            H = witness.H
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(check_cond1(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(check_cond2(G, H))
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(check_neg_q(G, H))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: There are no other subgroups of G having the same order as H",
    "¬Q: H is not a characteristic subgroup of G"
]
N_HYP = 2
NEG_Q_INDEX = 2