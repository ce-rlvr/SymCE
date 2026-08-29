import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'generate'):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def get_generators(group):
    if hasattr(group, 'generators'):
        return list(group.generators)
    else:
        return get_elements(group)

def inv(x):
    try:
        return ~x
    except Exception:
        return x**-1

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H_1: H is a subgroup of G
    h1 = False
    try:
        G, H, K = witness
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            G_elems = get_elements(G)
            h1 = all(h in G_elems for h in get_elements(H))
    except Exception:
        h1 = False

    # H_2: K is a subgroup of G
    h2 = False
    try:
        G, H, K = witness
        if hasattr(K, 'is_subgroup'):
            h2 = bool(K.is_subgroup(G))
        else:
            G_elems = get_elements(G)
            h2 = all(k in G_elems for k in get_elements(K))
    except Exception:
        h2 = False

    # ¬Q: H is contained in N_G(K) if and only if commutator(H, K) is a subset of K is FALSE
    neg_q = False
    try:
        G, H, K = witness
        K_elems = get_elements(K)
        
        # Check H <= N_G(K)
        H_in_N = True
        for h in get_generators(H):
            for k in get_generators(K):
                if (h * k * inv(h)) not in K_elems or (inv(h) * k * h) not in K_elems:
                    H_in_N = False
                    break
            if not H_in_N:
                break
        
        # Check commutator(H, K) <= K
        comm_in_K = True
        for h in get_elements(H):
            for k in get_elements(K):
                if (inv(h) * inv(k) * h * k) not in K_elems:
                    comm_in_K = False
                    break
            if not comm_in_K:
                break
        
        neg_q = not (H_in_N == comm_in_K)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "¬Q: H is contained in N_G(K) iff commutator of H and K is a subset of K is false"
]

N_HYP = 2
NEG_Q_INDEX = 2