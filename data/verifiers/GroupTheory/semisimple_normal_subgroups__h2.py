import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.ntheory

# Top-level setup: named object bindings for witness expressions
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
trivial = PermutationGroup(Permutation(0))

# Helper functions to safely access SymPy properties/methods
def get_order(G):
    return G.order() if callable(G.order) else G.order

def get_center(G):
    return G.center() if callable(G.center) else G.center

def get_derived_subgroup(G):
    return G.derived_subgroup() if callable(G.derived_subgroup) else G.derived_subgroup

def get_elements(G):
    return list(G.elements() if callable(G.elements) else G.elements)

def get_generators(G):
    return list(G.generators() if callable(G.generators) else G.generators)

def group_contains(G, g):
    try:
        return G.contains(g)
    except Exception:
        return g in G

def is_identity(g):
    if hasattr(g, 'is_Identity'):
        return g.is_Identity
    return all(i == g(i) for i in range(g.size))

# Group theory predicates
def is_square_free_exponent(G):
    for g in get_elements(G):
        o = g.order() if callable(g.order) else g.order
        for p, e in sympy.ntheory.factorint(o).items():
            if e > 1:
                return False
    return True

def is_simple(G):
    o = get_order(G)
    if o == 1:
        return False
    if sympy.ntheory.isprime(o):
        return True
    if o < 60:
        return False
    
    elems = get_elements(G)
    for g in elems:
        if is_identity(g):
            continue
        gens = [h * g * ~h for h in elems]
        nc = PermutationGroup(gens)
        if get_order(nc) < o:
            return False
    return True

def is_semisimple_nonabelian(G):
    o = get_order(G)
    if o == 1:
        return True
    if is_simple(G):
        return True
    elems = get_elements(G)
    for g in elems:
        if is_identity(g):
            continue
        gens = [h * g * ~h for h in elems]
        nc = PermutationGroup(gens)
        nc_o = get_order(nc)
        if 1 < nc_o < o:
            centralizer_gens = []
            nc_gens = get_generators(nc)
            for x in elems:
                commutes = True
                for y in nc_gens:
                    if x * y != y * x:
                        commutes = False
                        break
                if commutes:
                    centralizer_gens.append(x)
            cg = PermutationGroup(centralizer_gens)
            if nc_o * get_order(cg) == o:
                return is_semisimple_nonabelian(nc) and is_semisimple_nonabelian(cg)
            else:
                return False
    return False

def is_direct_product_of_simple_groups(N):
    if get_order(N) == 1:
        return True
    
    Z = get_center(N)
    D = get_derived_subgroup(N)
    
    if not is_square_free_exponent(Z):
        return False
        
    if get_order(D) == 1:
        return get_order(N) == get_order(Z)
        
    if not is_semisimple_nonabelian(D):
        return False
        
    if get_order(N) != get_order(Z) * get_order(D):
        return False
        
    return True

def is_normal_subgroup(G, N):
    if not isinstance(N, PermutationGroup):
        return False
    N_gens = get_generators(N)
    G_gens = get_generators(G)
    for gen in N_gens:
        if not group_contains(G, gen):
            return False
    for n in N_gens:
        for g in G_gens:
            if not group_contains(N, g * n * ~g):
                return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = is_normal_subgroup(G, N)
    except Exception:
        h2 = False
        
    # ¬Q: N is not isomorphic to a direct product of a subset of the simple factors of G
    # (Equivalent to N not being a direct product of simple groups)
    try:
        neg_q = not is_direct_product_of_simple_groups(N)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not isomorphic to a direct product of a subset of the simple factors of G"
]

N_HYP = 2
NEG_Q_INDEX = 2