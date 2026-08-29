import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy import oo

# Top-level setup for potential witness expressions
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

def is_group(G):
    if hasattr(G, 'is_group'):
        val = G.is_group
        return bool(val() if callable(val) else val)
    if hasattr(G, 'generators'):
        return True
    return False

def is_subgroup(sub, parent):
    if hasattr(sub, 'is_subgroup'):
        return bool(sub.is_subgroup(parent))
    if hasattr(parent, 'has_subgroup'):
        return bool(parent.has_subgroup(sub))
    try:
        if hasattr(sub, 'generators'):
            return all(g in parent for g in sub.generators)
    except Exception:
        pass
    return True

def get_index(parent, sub):
    if hasattr(parent, 'index'):
        try:
            return parent.index(sub)
        except Exception:
            pass
    if hasattr(parent, 'order') and hasattr(sub, 'order'):
        o_p = parent.order()
        o_s = sub.order()
        if o_p == oo and o_s == oo:
            raise ValueError("Cannot compute index of infinite groups without an explicit index method")
        return o_p / o_s
    raise ValueError("Objects do not have an index or order method")

def is_finite_index(idx):
    try:
        if idx == oo or idx == float('inf'):
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = is_group(H) and is_subgroup(H, G)
    except Exception:
        h2 = False

    # H3: K is a subgroup of H
    try:
        h3 = is_group(K) and is_subgroup(K, H)
    except Exception:
        h3 = False

    # H4: The index of K in H is finite
    try:
        idx_K_H = get_index(H, K)
        h4 = is_finite_index(idx_K_H)
    except Exception:
        h4 = False

    # neg_Q: The index of K in G is finite and equals the product of the index of H in G and the index of K in H.
    # We must return True if this conclusion FAILS.
    try:
        idx_K_G = get_index(G, K)
        idx_H_G = get_index(G, H)
        idx_K_H = get_index(H, K)
        
        if not is_finite_index(idx_K_G):
            concl = False
        else:
            concl = (idx_K_G == idx_H_G * idx_K_H)
            
        neg_q = not concl
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of H",
    "H_4: The index of K in H is finite",
    "not Q: The index of K in G is infinite or does not equal the product of indices"
]

N_HYP = 4
NEG_Q_INDEX = 4