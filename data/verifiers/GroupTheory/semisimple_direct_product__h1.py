import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, DirectProduct
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = DirectProduct(Z2, Z2)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_product_of_simple_orders(n):
    """
    Checks if n is a product of orders of known non-abelian simple groups.
    Includes orders of all non-abelian simple groups up to ~10000.
    """
    if n == 1:
        return True
    simple_orders = [
        60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 
        4080, 5616, 6048, 6072, 7800, 7920, 9828
    ]
    for so in simple_orders:
        if n % so == 0:
            if is_product_of_simple_orders(n // so):
                return True
    return False

def is_dp_nonabelian_simple(G):
    """
    Checks if a finite group G is isomorphic to a direct product of non-abelian simple groups.
    For small groups, this is equivalent to being perfect, centerless, and having an order 
    that is a product of orders of non-abelian simple groups.
    """
    try:
        order = G.order() if callable(G.order) else G.order
        if order == 1:
            return True
        
        is_ab = G.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
        if is_ab:
            return False
            
        der = G.derived_subgroup()
        der_order = der.order() if callable(der.order) else der.order
        if der_order != order:
            return False
            
        cen = G.center()
        cen_order = cen.order() if callable(cen.order) else cen.order
        if cen_order > 1:
            return False
            
        if not is_product_of_simple_orders(order):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G1, G2), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        G1, G2 = witness
    except Exception:
        return [False, False]
    
    # H_1: G_2 is a finite group that is isomorphic to a direct product of non-abelian simple groups
    try:
        h1_ok = is_dp_nonabelian_simple(G2)
    except Exception:
        h1_ok = False
        
    # Conclusion Q: The direct product G_1 \times G_2 is isomorphic to a direct product of non-abelian simple groups.
    # We want neg_Q to be True when Q fails.
    try:
        G1_G2 = DirectProduct(G1, G2)
        q_holds = is_dp_nonabelian_simple(G1_G2)
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G_2 is a finite group that is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: The direct product G_1 x G_2 is not isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 1
NEG_Q_INDEX = 1