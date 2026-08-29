import sympy
from sympy.combinatorics import PermutationGroup, Permutation, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = DirectProduct(Z2, Z2)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, K = witness
        if isinstance(G, list):
            G = PermutationGroup(G)
        if isinstance(H, list):
            H = PermutationGroup(H)
        if isinstance(K, list):
            K = PermutationGroup(K)
    except Exception:
        return [False, False, False, False, False]

    # H1: H is a normal subgroup of G
    try:
        h1 = True
        for h in H.generators:
            if h not in G:
                h1 = False
                break
        if h1:
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        h1 = False
                        break
                    if (~g * h * g) not in H:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: K is a normal subgroup of G
    try:
        h2 = True
        for k in K.generators:
            if k not in G:
                h2 = False
                break
        if h2:
            for g in G.generators:
                for k in K.generators:
                    if (g * k * ~g) not in K:
                        h2 = False
                        break
                    if (~g * k * g) not in K:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: The intersection of H and K contains only the identity element of G
    try:
        h3 = True
        for h_elem in H.elements:
            if h_elem in K and h_elem != G.identity:
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: G is equal to the product set HK
    try:
        if G.order() > H.order() * K.order():
            h4 = False
        else:
            hk_set = set()
            for h_elem in H.elements:
                for k_elem in K.elements:
                    hk_set.add(h_elem * k_elem)
            h4 = (hk_set == set(G.elements))
    except Exception:
        h4 = False

    # neg_Q: G is not isomorphic to the external direct product H × K
    try:
        HxK = DirectProduct(H, K)
        neg_q = not G.is_isomorphic(HxK)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: K is a normal subgroup of G",
    "H_3: The intersection of H and K contains only the identity element of G",
    "H_4: G is equal to the product set HK",
    "¬Q: G is not isomorphic to the external direct product H × K"
]

N_HYP = 4
NEG_Q_INDEX = 4