import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_identity(g):
    try:
        return g.is_Identity
    except Exception:
        try:
            return all(i == g(i) for i in range(g.size))
        except Exception:
            return False

def contains(G, g):
    try:
        if G.contains(g):
            return True
    except Exception:
        pass
    try:
        if is_identity(g):
            return True
    except Exception:
        pass
    try:
        for x in G.generate():
            if x == g:
                return True
            size = max(x.size, g.size)
            if all(x(i) == g(i) for i in range(size)):
                return True
    except Exception:
        pass
    return False

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if not contains(G, h):
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    if not is_subgroup(N, G):
        return False
    try:
        for g in G.generators:
            for n in N.generators:
                if not contains(N, g * n * ~g):
                    return False
                if not contains(N, ~g * n * g):
                    return False
        return True
    except Exception:
        return False

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def is_abelian(G):
    try:
        return G.is_abelian
    except Exception:
        pass
    try:
        gens = G.generators
        for g1 in gens:
            for g2 in gens:
                if g1 * g2 != g2 * g1:
                    return False
        return True
    except Exception:
        return True

def are_isomorphic(G1, G2):
    if get_order(G1) != get_order(G2):
        return False
    if is_abelian(G1) != is_abelian(G2):
        return False
    
    def element_orders(G):
        orders = {}
        for g in G.generate():
            try:
                o = g.order()
            except TypeError:
                o = g.order
            orders[o] = orders.get(o, 0) + 1
        return orders
        
    if element_orders(G1) != element_orders(G2):
        return False
        
    try:
        return G1.is_isomorphic(G2)
    except Exception:
        pass
    return True

def quotient_group_and_subgroup(G, N, K):
    G_els = list(G.generate())
    N_els = set(N.generate())
    
    cosets = []
    coset_reps = []
    seen = set()
    for g in G_els:
        if g not in seen:
            coset = set(g * n for n in N_els)
            cosets.append(coset)
            coset_reps.append(g)
            seen.update(coset)
            
    def get_perms(generators):
        perms = []
        for gen in generators:
            p = []
            for rep in coset_reps:
                target = gen * rep
                found = False
                for j, c in enumerate(cosets):
                    if target in c:
                        p.append(j)
                        found = True
                        break
                if not found:
                    p.append(0)
            perms.append(Permutation(p))
        return perms

    degree = len(cosets)
    id_perm = Permutation(degree - 1) if degree > 0 else Permutation(0)
    
    G_mod_N_perms = get_perms(G.generators)
    K_mod_N_perms = get_perms(K.generators)
    
    G_mod_N = PermutationGroup(G_mod_N_perms or [id_perm])
    K_mod_N = PermutationGroup(K_mod_N_perms or [id_perm])
    
    return G_mod_N, K_mod_N

def quotient_group(G, N):
    if not is_normal(N, G):
        return None
    G_els = list(G.generate())
    N_els = set(N.generate())
    
    cosets = []
    coset_reps = []
    seen = set()
    for g in G_els:
        if g not in seen:
            coset = set(g * n for n in N_els)
            cosets.append(coset)
            coset_reps.append(g)
            seen.update(coset)
            
    perms = []
    for gen in G.generators:
        p = []
        for rep in coset_reps:
            target = gen * rep
            found = False
            for j, c in enumerate(cosets):
                if target in c:
                    p.append(j)
                    found = True
                    break
            if not found:
                p.append(0)
        perms.append(Permutation(p))
        
    degree = len(cosets)
    id_perm = Permutation(degree - 1) if degree > 0 else Permutation(0)
    return PermutationGroup(perms or [id_perm])

def conditions(witness):
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_normal(N, G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal(K, G)
    except Exception:
        h2 = False
        
    try:
        h3 = is_subgroup(N, K)
    except Exception:
        h3 = False
        
    try:
        if not is_subgroup(K, G):
            q = False
        elif not is_normal(N, G) or not is_normal(N, K) or not is_normal(K, G):
            q = False
        else:
            G_mod_N, K_mod_N = quotient_group_and_subgroup(G, N, K)
            if not is_normal(K_mod_N, G_mod_N):
                q = False
            else:
                G_mod_N_mod_K_mod_N = quotient_group(G_mod_N, K_mod_N)
                G_mod_K = quotient_group(G, K)
                if G_mod_N_mod_K_mod_N is None or G_mod_K is None:
                    q = False
                else:
                    q = are_isomorphic(G_mod_N_mod_K_mod_N, G_mod_K)
    except Exception:
        q = False
        
    neg_q = not q
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: K is a normal subgroup of G",
    "H_3: N is a subset of K",
    "¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K"
]

N_HYP = 3
NEG_Q_INDEX = 3