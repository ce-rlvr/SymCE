import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: The index of H in G is finite",
    "not Q: The intersection of H and K has infinite index in G, or index of H cap K in G > index of H in G * index of K in G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, K = witness
        elif isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            K = witness['K']
        else:
            G = witness.G
            H = witness.H
            K = witness.K
    except Exception:
        return [False, False, False, False, False]

    def is_group(X):
        if isinstance(X, int):
            return True
        if hasattr(X, 'is_group'):
            attr = X.is_group
            if callable(attr):
                return attr()
            return attr
        if hasattr(X, 'generators'):
            return True
        return True

    def is_subgroup(sub, grp):
        if isinstance(sub, int) and isinstance(grp, int):
            if grp == 0:
                return sub == 0
            return sub % grp == 0
        if hasattr(sub, 'is_subgroup'):
            attr = sub.is_subgroup
            if callable(attr):
                return attr(grp)
            return attr
        if hasattr(grp, 'has_subgroup'):
            attr = grp.has_subgroup
            if callable(attr):
                return attr(sub)
            return attr
        if hasattr(sub, 'generators') and hasattr(grp, 'contains'):
            try:
                return all(grp.contains(g) for g in sub.generators)
            except Exception:
                pass
        return True

    def get_index(grp, sub):
        if isinstance(grp, int) and isinstance(sub, int):
            if sub == 0:
                return math.inf if grp != 0 else 1
            if grp == 0:
                return math.inf
            if sub % grp == 0:
                return abs(sub // grp)
            return math.inf
        if hasattr(grp, 'order') and hasattr(sub, 'order'):
            try:
                return grp.order() // sub.order()
            except Exception:
                pass
        if hasattr(grp, 'index'):
            attr = grp.index
            if callable(attr):
                return attr(sub)
            return attr
        if hasattr(sub, 'index_in'):
            attr = sub.index_in
            if callable(attr):
                return attr(grp)
            return attr
        raise ValueError("Cannot compute index")

    def get_intersection(h, k):
        if isinstance(h, int) and isinstance(k, int):
            if h == 0 or k == 0:
                return 0
            return abs(h * k) // math.gcd(h, k)
        if hasattr(h, 'intersection'):
            attr = h.intersection
            if callable(attr):
                return attr(k)
            return attr
        if hasattr(h, 'intersect'):
            attr = h.intersect
            if callable(attr):
                return attr(k)
            return attr
        raise ValueError("Cannot compute intersection")

    try:
        h1 = bool(is_group(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_subgroup(H, G))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_subgroup(K, G))
    except Exception:
        h3 = False

    try:
        idx_H = get_index(G, H)
        h4 = (idx_H < math.inf)
    except Exception:
        h4 = False

    try:
        idx_K = get_index(G, K)
        H_cap_K = get_intersection(H, K)
        idx_H_cap_K = get_index(G, H_cap_K)
        
        conclusion = (idx_H_cap_K < math.inf) and (idx_H_cap_K <= idx_H * idx_K)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]