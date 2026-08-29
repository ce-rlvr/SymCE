import sympy
from sympy.combinatorics import PermutationGroup, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups",
    "H_2: H is a subnormal subgroup of G",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_finite_semisimple(G):
    """Fallback check for finite SymPy groups."""
    if not hasattr(G, 'order') or not hasattr(G, 'derived_subgroup') or not hasattr(G, 'center'):
        return False
    if G.order() == 1:
        return False
    if G.derived_subgroup().order() != G.order():
        return False
    if G.center().order() != 1:
        return False
    
    # Orders of non-abelian simple groups up to ~10000
    SIMPLE_ORDERS = [60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080, 5616, 6048, 7920, 9828]
    def is_prod(n):
        if n == 1: return True
        for o in SIMPLE_ORDERS:
            if n % o == 0:
                if is_prod(n // o): return True
        return False
    return is_prod(G.order())

def check_finite_subnormal(G, H):
    """Fallback check for finite SymPy groups."""
    if not hasattr(G, 'contains') or not hasattr(H, 'generators'):
        return False
    if H.order() == 1:
        return True
    for g in H.generators:
        if not G.contains(g):
            return False
    current = G
    while True:
        gens = list(H.generators)
        group = PermutationGroup(gens)
        while True:
            new_gens = list(group.generators)
            for g in current.generators:
                for h in group.generators:
                    conj = g * h * ~g
                    new_gens.append(conj)
            new_group = PermutationGroup(new_gens)
            if new_group.order() == group.order():
                break
            group = new_group
        if group.order() == current.order():
            break
        current = group
    return current.order() == H.order()

def check_finite_normal(G, H):
    """Fallback check for finite SymPy groups."""
    if not hasattr(G, 'contains') or not hasattr(H, 'generators'):
        return False
    if H.order() == 1:
        return True
    for g in H.generators:
        if not G.contains(g):
            return False
    for g in G.generators:
        for h in H.generators:
            conj = g * h * ~g
            if not H.contains(conj):
                return False
    return True

def get_bool_attr(obj, attr_name, *args):
    attr = getattr(obj, attr_name)
    if callable(attr):
        try:
            return bool(attr(*args))
        except TypeError:
            return bool(attr())
    return bool(attr)

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
    elif isinstance(witness, tuple) and len(witness) == 2:
        G, H = witness
    else:
        G = witness
        H = getattr(witness, 'H', None)

    # H1: G is isomorphic to a direct product of non-abelian simple groups
    h1 = False
    try:
        if hasattr(G, 'is_isomorphic_to_direct_product_of_nonabelian_simple_groups'):
            h1 = get_bool_attr(G, 'is_isomorphic_to_direct_product_of_nonabelian_simple_groups')
        elif hasattr(G, 'is_direct_product_of_nonabelian_simple_groups'):
            h1 = get_bool_attr(G, 'is_direct_product_of_nonabelian_simple_groups')
        elif hasattr(G, 'is_semisimple'):
            h1 = get_bool_attr(G, 'is_semisimple')
        else:
            h1 = check_finite_semisimple(G)
    except Exception:
        pass

    # H2: H is a subnormal subgroup of G
    h2 = False
    try:
        if hasattr(H, 'is_subnormal_in'):
            h2 = get_bool_attr(H, 'is_subnormal_in', G)
        elif hasattr(G, 'is_subnormal_subgroup'):
            h2 = get_bool_attr(G, 'is_subnormal_subgroup', H)
        elif hasattr(H, 'is_subnormal'):
            h2 = get_bool_attr(H, 'is_subnormal', G)
        else:
            h2 = check_finite_subnormal(G, H)
    except Exception:
        pass

    # neg_Q: H is NOT a normal subgroup of G
    neg_q = False
    try:
        if hasattr(H, 'is_normal_in'):
            neg_q = not get_bool_attr(H, 'is_normal_in', G)
        elif hasattr(G, 'is_normal_subgroup'):
            neg_q = not get_bool_attr(G, 'is_normal_subgroup', H)
        elif hasattr(H, 'is_normal'):
            neg_q = not get_bool_attr(H, 'is_normal', G)
        else:
            neg_q = not check_finite_normal(G, H)
    except Exception:
        pass

    return [h1, h2, neg_q]