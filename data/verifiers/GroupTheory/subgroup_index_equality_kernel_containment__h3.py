import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, f, A, B = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
    except Exception:
        G_elems = []
        
    try:
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
    except Exception:
        H_elems = []

    try:
        if isinstance(f, dict):
            f_map = f
        else:
            f_map = {g: f(g) for g in G_elems}
    except Exception:
        f_map = {}

    # H1: G and H are groups
    try:
        h1 = len(G_elems) > 0 and len(H_elems) > 0
    except Exception:
        h1 = False

    # H2: f is a surjective group homomorphism
    try:
        f_values = set(f_map.values())
        H_set = set(H_elems)
        is_surjective = (f_values == H_set) and len(H_set) > 0
        
        is_homo = True
        for g1 in G_elems:
            for g2 in G_elems:
                if f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                    is_homo = False
                    break
            if not is_homo:
                break
        h2 = is_surjective and is_homo
    except Exception:
        h2 = False

    # H3: The kernel of f is a subgroup of A
    try:
        if hasattr(H, 'identity'):
            H_id = H.identity
        else:
            H_id = next(h for h in H_elems if h * h == h)
            
        ker = {g for g in G_elems if f_map[g] == H_id}
        A_elems = set(A.elements) if hasattr(A, 'elements') else set(A)
        h3 = ker.issubset(A_elems)
    except Exception:
        h3 = False

    # neg_Q: The index of A in B is not equal to the index of f(A) in f(B)
    try:
        B_elems = set(B.elements) if hasattr(B, 'elements') else set(B)
        f_B = set(f_map[b] for b in B_elems)
        f_A = set(f_map[a] for a in A_elems)
        
        neg_q = len(B_elems) * len(f_A) != len(A_elems) * len(f_B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism from G to H",
    "H_3: The kernel of f is a subgroup of A",
    "¬Q: The index of A in B is not equal to the index of f(A) in f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3