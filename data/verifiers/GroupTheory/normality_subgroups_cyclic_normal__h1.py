import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
        return all(G.contains(h) for h in H.generators)
    except Exception:
        return False

def is_normal(H, G):
    try:
        if hasattr(H, 'is_normal'):
            return H.is_normal(G)
        if not is_subgroup(H, G):
            return False
        for h in H.generators:
            for g in G.generators:
                if not H.contains(g * h * ~g):
                    return False
                if not H.contains(~g * h * g):
                    return False
        return True
    except Exception:
        return False

def is_cyclic(G):
    try:
        is_cyc = getattr(G, 'is_cyclic', None)
        if is_cyc is not None:
            return bool(is_cyc)
        
        order = G.order()
        for g in G.generate():
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: Let N be a normal subgroup of G
    try:
        h1_ok = is_normal(N, G)
    except Exception:
        h1_ok = False

    # H_2: N is a cyclic group
    try:
        h2_ok = is_cyclic(N)
    except Exception:
        h2_ok = False

    # H_3: Let H be a subgroup of N
    try:
        h3_ok = is_subgroup(H, N)
    except Exception:
        h3_ok = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        neg_q_ok = not is_normal(H, G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a cyclic group",
    "H_3: H is a subgroup of N",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3