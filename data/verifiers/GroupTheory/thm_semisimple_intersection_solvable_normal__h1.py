import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_order(G):
    order = G.order
    if callable(order):
        return order()
    return order

def get_center(G):
    c = G.center
    if callable(c):
        return c()
    return c

def get_derived_subgroup(G):
    ds = G.derived_subgroup
    if callable(ds):
        return ds()
    return ds

def get_normal_subgroups(G):
    ns = G.normal_subgroups
    if callable(ns):
        return ns()
    return ns

def check_solvable(G):
    solv = G.is_solvable
    if callable(solv):
        return solv()
    return solv

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(H, G):
    if not is_subgroup(H, G):
        return False
    try:
        for g in G.generators:
            for h in H.generators:
                conj = (g**-1) * h * g
                if conj not in H:
                    return False
        return True
    except Exception:
        return False

def is_semisimple(G):
    try:
        normal_subgroups = get_normal_subgroups(G)
    except Exception:
        return False
    
    def is_comp_red(G, normal_subgroups):
        g_order = get_order(G)
        for H in normal_subgroups:
            has_complement = False
            for K in normal_subgroups:
                if get_order(H) * get_order(K) == g_order:
                    I = H.intersect(K)
                    if get_order(I) == 1:
                        has_complement = True
                        break
            if not has_complement:
                return False
        return True

    # Check if G is a direct product of simple groups (completely reducible)
    if is_comp_red(G, normal_subgroups):
        return True
        
    # Check if G is a central product of quasisimple groups
    try:
        if get_order(get_derived_subgroup(G)) == get_order(G):
            Z = get_center(G)
            z_order = get_order(Z)
            g_order = get_order(G)
            for H in normal_subgroups:
                if not is_subgroup(Z, H): continue
                has_complement = False
                for K in normal_subgroups:
                    if not is_subgroup(Z, K): continue
                    if get_order(H) * get_order(K) // z_order == g_order:
                        I = H.intersect(K)
                        if get_order(I) == z_order:
                            has_complement = True
                            break
                if not has_complement:
                    return False
            return True
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    try:
        G, N, S = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_normal_subgroup(N, G) and is_semisimple(N))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_normal_subgroup(S, G) and check_solvable(S))
    except Exception:
        h2 = False
        
    try:
        neg_q = not (get_order(N.intersect(S)) == 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal semisimple subgroup of G",
    "H_2: S is a normal solvable subgroup of G",
    "¬Q: The intersection of N and S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2