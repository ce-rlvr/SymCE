import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: G is a finite semisimple group",
    "H_2: G is the direct product of exactly k pairwise non-isomorphic simple groups",
    "¬Q: G does not have exactly 2^k distinct normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_simple_group(H):
    """Helper to check if a group is simple."""
    if H.order() == 1:
        return False
    return len(H.normal_subgroups()) == 2

def conditions(witness) -> list[bool]:
    # The witness can be a tuple (G, k) or just G
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        G, k = witness
    else:
        G = witness
        k = None

    # H_1: G is a finite semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    try:
        h1 = True
        for N in G.normal_subgroups():
            if N.order() > 1 and N.is_abelian:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: G is the direct product of exactly k pairwise non-isomorphic simple groups
    try:
        simple_normals = []
        for N in G.normal_subgroups():
            if is_simple_group(N):
                simple_normals.append(N)
        
        computed_k = len(simple_normals)
        
        product_order = 1
        for N in simple_normals:
            product_order *= N.order()
            
        is_direct_product = (product_order == G.order())
        
        orders = [N.order() for N in simple_normals]
        pairwise_non_iso = (len(set(orders)) == len(orders))
        
        if k is not None:
            h2 = is_direct_product and pairwise_non_iso and (computed_k == k)
        else:
            h2 = is_direct_product and pairwise_non_iso
            k = computed_k
    except Exception:
        h2 = False

    # ¬Q: G does not have exactly 2^k distinct normal subgroups
    try:
        if k is None:
            neg_q = False
        else:
            num_normal = len(G.normal_subgroups())
            q = (num_normal == 2**k)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]