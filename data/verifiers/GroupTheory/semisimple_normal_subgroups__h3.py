import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_composition_factor_orders(G):
    if G.order() == 1:
        return []
    series = G.composition_series()
    orders = []
    for i in range(len(series)-1):
        orders.append(series[i].order() // series[i+1].order())
    return sorted(orders)

def is_dp_nonabelian_simple(G):
    """
    A finite group is a direct product of non-abelian simple groups
    if and only if all of its composition factors are non-abelian simple groups.
    A simple group is non-abelian iff its order is not prime.
    """
    if G.order() == 1:
        return True
    try:
        orders = get_composition_factor_orders(G)
        if not orders:
            return False
        for o in orders:
            if sympy.ntheory.isprime(o):
                return False
        return True
    except Exception:
        return False

def conclusion_holds(G, N):
    """
    Checks if N is the trivial subgroup or isomorphic to a direct product
    of a subset of the simple factors of G.
    """
    if N.order() == 1:
        return True
    
    # N must itself be a direct product of non-abelian simple groups
    if not is_dp_nonabelian_simple(N):
        return False
        
    g_orders = get_composition_factor_orders(G)
    n_orders = get_composition_factor_orders(N)
    
    # The composition factors of N must be a sub-multiset of those of G
    g_orders_copy = list(g_orders)
    for o in n_orders:
        if o in g_orders_copy:
            g_orders_copy.remove(o)
        else:
            return False
            
    return True

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = G.order() >= 1
    except Exception:
        h1 = False
        
    # H_2: G is isomorphic to a direct product of non-abelian simple groups
    try:
        h2 = is_dp_nonabelian_simple(G)
    except Exception:
        h2 = False
        
    # neg_Q: N is neither the trivial subgroup nor isomorphic to a direct product of a subset of the simple factors
    try:
        q = conclusion_holds(G, N)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: N is neither the trivial subgroup nor isomorphic to a direct product of a subset of the simple factors"
]

N_HYP = 2
NEG_Q_INDEX = 2