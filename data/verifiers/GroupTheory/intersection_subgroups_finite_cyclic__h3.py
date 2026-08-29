import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (G, H, K).
    """
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite cyclic group
    try:
        is_cyc = G.is_cyclic
        if callable(is_cyc):
            is_cyc = is_cyc()
            
        g_order = G.order
        if callable(g_order):
            g_order = g_order()
            
        h1 = bool(is_cyc and g_order > 0 and g_order < float('inf'))
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False
        
    # ¬Q: The order of the intersection H \cap K is NOT equal to gcd(|H|, |K|)
    try:
        h_elems = H.elements
        if callable(h_elems):
            h_elems = h_elems()
        h_elems = set(h_elems)
        
        k_elems = K.elements
        if callable(k_elems):
            k_elems = k_elems()
        k_elems = set(k_elems)
        
        intersection_order = len(h_elems.intersection(k_elems))
        
        h_order = H.order
        if callable(h_order):
            h_order = h_order()
            
        k_order = K.order
        if callable(k_order):
            k_order = k_order()
            
        expected_order = math.gcd(int(h_order), int(k_order))
        
        neg_q = bool(intersection_order != expected_order)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: H is a subgroup of G",
    "¬Q: The order of the intersection H \\cap K is not equal to gcd(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2