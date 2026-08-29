import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
from collections import Counter

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
    "H_1: G is a group and H, K are subgroups",
    "H_2: K is a normal subgroup of G",
    "H_3: Intersection of H and K is trivial",
    "H_4: G is equal to the product set HK",
    "¬Q: G is not isomorphic to H x K"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    def get_order(group):
        if hasattr(group, 'order'):
            o = group.order
            if callable(o):
                return o()
            return o
        return len(list(group.elements))

    def get_elem_order(elem):
        if hasattr(elem, 'order'):
            o = elem.order
            if callable(o):
                return o()
            return o
        return 1

    def get_elements(group):
        e = group.elements
        if callable(e):
            return list(e())
        return list(e)

    def is_abelian(group):
        if hasattr(group, 'is_abelian'):
            a = group.is_abelian
            if callable(a):
                return a()
            return a
        for g1 in group.generators:
            for g2 in group.generators:
                if g1 * g2 != g2 * g1:
                    return False
        return True

    # H1: G is a group, H and K are subgroups
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)):
            h1 = False
        else:
            h1 = all(g in G for g in H.generators) and all(g in G for g in K.generators)
    except Exception:
        h1 = False

    # H2: K is a normal subgroup of G
    try:
        h2 = True
        for k in K.generators:
            for g in G.generators:
                if (g * k * ~g) not in K:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: Intersection of H and K is trivial
    try:
        g_elems = get_elements(G)
        h_elems = get_elements(H)
        id_G = next(g for g in g_elems if get_elem_order(g) == 1)
        h3 = True
        for h in h_elems:
            if h in K and h != id_G:
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: G is equal to the product set HK
    try:
        h_elems = get_elements(H)
        k_elems = get_elements(K)
        hk_set = set(h * k for h in h_elems for k in k_elems)
        h4 = (len(hk_set) == get_order(G))
    except Exception:
        h4 = False

    # neg_Q: G is not isomorphic to H x K
    try:
        def lcm(a, b):
            return abs(a*b) // math.gcd(a, b)
            
        g_elems = get_elements(G)
        h_elems = get_elements(H)
        k_elems = get_elements(K)
        
        g_orders = Counter(get_elem_order(g) for g in g_elems)
        hk_orders = Counter(lcm(get_elem_order(h), get_elem_order(k)) for h in h_elems for k in k_elems)
        
        hk_is_abelian = is_abelian(H) and is_abelian(K)
        
        if is_abelian(G) != hk_is_abelian:
            neg_q = True
        elif g_orders != hk_orders:
            neg_q = True
        else:
            g_center_size = len([g for g in g_elems if all(g*x == x*g for x in g_elems)])
            h_center_size = len([h for h in h_elems if all(h*x == x*h for x in h_elems)])
            k_center_size = len([k for k in k_elems if all(k*x == x*k for x in k_elems)])
            if g_center_size != h_center_size * k_center_size:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]