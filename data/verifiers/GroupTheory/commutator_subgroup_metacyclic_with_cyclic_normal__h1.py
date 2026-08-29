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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_cyclic(H):
    try:
        is_cyc = getattr(H, 'is_cyclic', None)
        if is_cyc is True:
            return True
        if is_cyc is False:
            return False
    except Exception:
        pass
    
    try:
        order = H.order()
        if order == 1:
            return True
        for g in H.elements:
            if g.order() == order:
                return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        h1 = False
        if N.is_subgroup(G):
            h1 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * (g**-1)) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: N is a cyclic group
    try:
        h2 = is_cyclic(N)
    except Exception:
        h2 = False

    # H3: The quotient group G/N is a cyclic group
    try:
        h3 = False
        if h1:
            target_order = G.order() // N.order()
            for g in G.elements:
                k = 1
                curr = g
                while curr not in N and k <= target_order:
                    curr = curr * g
                    k += 1
                if k == target_order and curr in N:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup G' is not a cyclic group
    try:
        C = G.derived_subgroup()
        neg_q = not is_cyclic(C)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a cyclic group",
    "H_3: The quotient group G/N is a cyclic group",
    "¬Q: The commutator subgroup G' is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3