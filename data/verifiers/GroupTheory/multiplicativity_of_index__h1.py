import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(sub, super_group):
    if hasattr(sub, 'is_subgroup'):
        try:
            return sub.is_subgroup(super_group)
        except Exception:
            pass
    if hasattr(sub, 'generators') and hasattr(super_group, '__contains__'):
        try:
            return all(g in super_group for g in sub.generators)
        except Exception:
            pass
    if hasattr(sub, '__iter__') and hasattr(super_group, '__contains__'):
        try:
            return all(x in super_group for x in sub)
        except Exception:
            pass
    return False

def get_index(super_group, sub):
    if hasattr(super_group, 'order') and hasattr(sub, 'order'):
        o_sup = super_group.order()
        o_sub = sub.order()
        if o_sub == 0 or o_sup == oo or o_sup == float('inf'):
            raise ValueError("Infinite or undefined index")
        if o_sup % o_sub != 0:
            raise ValueError("Index is not an integer")
        return o_sup // o_sub
        
    if hasattr(super_group, '__len__') and hasattr(sub, '__len__'):
        l_sup = len(super_group)
        l_sub = len(sub)
        if l_sub == 0:
            raise ValueError("Zero length subgroup")
        if l_sup % l_sub != 0:
            raise ValueError("Index is not an integer")
        return l_sup // l_sub
        
    raise ValueError("Cannot compute index")

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = bool(is_subgroup(H, G))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_subgroup(K, H))
    except Exception:
        h2 = False

    try:
        idx_H_G = get_index(G, H)
        h3 = True
    except Exception:
        h3 = False

    try:
        idx_K_H = get_index(H, K)
        h4 = True
    except Exception:
        h4 = False

    try:
        idx_K_G = get_index(G, K)
        idx_H_G = get_index(G, H)
        idx_K_H = get_index(H, K)
        q = (idx_K_G == idx_H_G * idx_K_H)
        neg_q = not q
    except Exception:
        # If the index of K in G cannot be computed (e.g., it is infinite or undefined),
        # then the conclusion that it is finite and equals the product fails.
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of H",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in H is finite",
    "¬Q: The index of K in G is not finite or does not equal the product of the index of H in G and the index of K in H"
]

N_HYP = 4
NEG_Q_INDEX = 4