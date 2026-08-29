import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = hasattr(G, 'is_group') and G.is_group
        if not h1:
            h1 = hasattr(G, 'generate') and hasattr(G, 'identity')
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = H.is_subgroup(G)
        else:
            H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H)
            G_elements = list(G.generate())
            if not H_elements:
                h2 = False
            else:
                h2 = all(g in G_elements for g in H_elements)
                is_closed = all(a * b in H_elements for a in H_elements for b in H_elements)
                has_inv = all(a**-1 in H_elements for a in H_elements)
                h2 = h2 and is_closed and has_inv
    except Exception:
        h2 = False

    # neg_Q: H is contained in N_G(K) iff [H, K] \subseteq K (must FAIL)
    try:
        H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H)
        K_elements = list(K.generate()) if hasattr(K, 'generate') else list(K)
        K_set = set(K_elements)

        # Check H \subseteq N_G(K)
        H_in_N_G_K = True
        for h in H_elements:
            h_K_h_inv = {h * k * h**-1 for k in K_set}
            if h_K_h_inv != K_set:
                H_in_N_G_K = False
                break

        # Check [H, K] \subseteq K
        # We compute the commutator subgroup under both standard conventions to be robust
        comm_set1 = {h**-1 * k**-1 * h * k for h in H_elements for k in K_set}
        comm_set2 = {h * k * h**-1 * k**-1 for h in H_elements for k in K_set}

        sub1 = set(PermutationGroup(*list(comm_set1)).generate()) if comm_set1 else set()
        sub2 = set(PermutationGroup(*list(comm_set2)).generate()) if comm_set2 else set()

        in1 = sub1.issubset(K_set)
        in2 = sub2.issubset(K_set)

        # The conclusion is H_in_N_G_K <==> [H, K] \subseteq K
        # It fails if H_in_N_G_K differs from the truth value of [H, K] \subseteq K
        # We consider it a failure if it fails under ANY of the two standard commutator conventions
        neg_q = (H_in_N_G_K != in1) or (H_in_N_G_K != in2)

    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The equivalence fails"
]

N_HYP = 2
NEG_Q_INDEX = 2