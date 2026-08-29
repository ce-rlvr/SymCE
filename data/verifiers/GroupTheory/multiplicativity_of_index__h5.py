import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo
import math

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

def check_is_group(obj):
    if hasattr(obj, 'is_group'):
        if callable(obj.is_group):
            return bool(obj.is_group())
        return bool(obj.is_group)
    if isinstance(obj, PermutationGroup):
        return True
    return False

def check_is_subgroup(sub, parent):
    if hasattr(sub, 'is_subgroup'):
        if callable(sub.is_subgroup):
            return bool(sub.is_subgroup(parent))
        return bool(sub.is_subgroup)
    if hasattr(parent, 'has_subgroup'):
        if callable(parent.has_subgroup):
            return bool(parent.has_subgroup(sub))
    return False

def get_index(parent, sub):
    if hasattr(parent, 'index'):
        if callable(parent.index):
            return parent.index(sub)
    if hasattr(parent, 'index_of'):
        if callable(parent.index_of):
            return parent.index_of(sub)
    if hasattr(sub, 'index_in'):
        if callable(sub.index_in):
            return sub.index_in(parent)
    
    # Fallback to order division
    if hasattr(parent, 'order') and hasattr(sub, 'order'):
        o_p = parent.order() if callable(parent.order) else parent.order
        o_s = sub.order() if callable(sub.order) else sub.order
        if o_p == oo and o_s == oo:
            raise ValueError("Cannot compute index of infinite groups from orders alone")
        return o_p / o_s
    raise ValueError("Cannot compute index")

def is_finite(val):
    if val is None:
        return False
    try:
        if val == oo or val == math.inf or val == float('inf'):
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            K = witness['K']
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'K'):
            G = witness.G
            H = witness.H
            K = witness.K
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, K = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = check_is_group(G)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = check_is_group(H) and check_is_subgroup(H, G)
    except Exception:
        h2 = False

    # H3: K is a subgroup of H
    try:
        h3 = check_is_group(K) and check_is_subgroup(K, H)
    except Exception:
        h3 = False

    # H4: The index of H in G is finite
    try:
        idx_HG = get_index(G, H)
        h4 = is_finite(idx_HG)
    except Exception:
        h4 = False

    # neg_Q: The index of K in G is not finite OR does not equal index of H in G * index of K in H
    try:
        idx_KG = get_index(G, K)
        idx_KH = get_index(H, K)
        idx_HG = get_index(G, H)
        
        finite_KG = is_finite(idx_KG)
        
        if not finite_KG:
            neg_q = True
        else:
            neg_q = (idx_KG != idx_HG * idx_KH)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of H",
    "H_4: The index of H in G is finite",
    "¬Q: The index of K in G is not finite or does not equal the product of the index of H in G and the index of K in H"
]

N_HYP = 4
NEG_Q_INDEX = 4