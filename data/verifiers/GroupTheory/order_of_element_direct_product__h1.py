import math
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy import lcm

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: g is an element of G with finite order m",
    "H_2: h is an element of H with finite order n",
    "¬Q: The order of the element (g, h) in the direct product G × H is not lcm(m, n)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_group_order(G):
    if hasattr(G, 'order'):
        if callable(G.order):
            return int(G.order())
        else:
            return int(G.order)
    if hasattr(G, '__len__'):
        return len(G)
    raise ValueError("Cannot determine group order")

def get_elem_order(g, G=None):
    if hasattr(g, 'order'):
        if callable(g.order):
            return int(g.order())
        else:
            return int(g.order)
    if isinstance(g, (int, sympy.Integer)) and G is not None:
        m = get_group_order(G)
        return m // math.gcd(int(g), m)
    raise ValueError("Cannot determine element order")

def check_h(G, g, m):
    if not (g in G):
        return False
    m_int = int(m)
    if m_int <= 0:
        return False
    
    # Interpretation 1: G has order m
    try:
        if get_group_order(G) == m_int:
            return True
    except Exception:
        pass
        
    # Interpretation 2: g^m == e (m is a multiple of the exact order of g)
    try:
        exact_order = get_elem_order(g, G)
        if m_int % exact_order == 0:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        # The witness can explicitly provide m and n, or they can be inferred from the groups
        if len(witness) == 6:
            G, g, m, H, h, n = witness
        elif len(witness) == 4:
            G, g, H, h = witness
            m = get_group_order(G)
            n = get_group_order(H)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = check_h(G, g, m)
    except Exception:
        h1 = False

    try:
        h2 = check_h(H, h, n)
    except Exception:
        h2 = False

    try:
        g_order = int(get_elem_order(g, G))
        h_order = int(get_elem_order(h, H))
        m_int = int(m)
        n_int = int(n)
        
        # The actual order of (g, h) in G x H is lcm(|g|, |h|)
        actual_order = int(lcm(g_order, h_order))
        expected_order = int(lcm(m_int, n_int))
        
        neg_q = (actual_order != expected_order)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]