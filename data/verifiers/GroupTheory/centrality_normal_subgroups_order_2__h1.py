import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    def get_generators(grp):
        if hasattr(grp, 'generators'):
            return grp.generators
        return grp

    def contains(grp, x):
        if hasattr(grp, 'contains'):
            return grp.contains(x)
        return x in grp

    # H1: N is a normal subgroup of G
    try:
        is_subgroup = all(contains(G, n) for n in get_generators(N))
        is_normal = True
        if is_subgroup:
            for g in get_generators(G):
                for n in get_generators(N):
                    try:
                        g_inv = ~g
                    except Exception:
                        g_inv = g**-1
                    
                    conj = g_inv * n * g
                    if not contains(N, conj):
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1 = bool(is_subgroup and is_normal)
    except Exception:
        h1 = False

    # H2: The order of N is 2
    try:
        if hasattr(N, 'order'):
            if callable(N.order):
                order_N = N.order()
            else:
                order_N = N.order
        else:
            order_N = len(list(N))
        h2 = bool(order_N == 2)
    except Exception:
        h2 = False

    # neg_Q: N is NOT a subgroup of the center of G
    try:
        is_subgroup = all(contains(G, n) for n in get_generators(N))
        in_center = True
        for n in get_generators(N):
            for g in get_generators(G):
                if n * g != g * n:
                    in_center = False
                    break
            if not in_center:
                break
        neg_q = not (is_subgroup and in_center)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The order of N is 2",
    "¬Q: N is not a subgroup of the center Z(G) of G"
]

N_HYP = 2
NEG_Q_INDEX = 2