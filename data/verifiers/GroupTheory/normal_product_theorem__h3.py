import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects for witness namespace
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

# Standard linear algebra objects
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
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a normal subgroup of G
    try:
        h2 = bool(H.is_subgroup(G) and H.is_normal(G))
    except Exception:
        h2 = False

    # neg_Q: HK is not a normal subgroup of G
    try:
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        K_elems = list(K.elements) if hasattr(K, 'elements') else list(K)
        HK_set = set(h * k for h in H_elems for k in K_elems)
        
        # Find the identity element of G
        id_elem = next(x for x in G.elements if x.is_Identity)
        
        is_subgroup = True
        if not HK_set or id_elem not in HK_set:
            is_subgroup = False
        else:
            # Check closure under inversion
            for x in HK_set:
                if ~x not in HK_set:
                    is_subgroup = False
                    break
            # Check closure under multiplication
            if is_subgroup:
                for x in HK_set:
                    for y in HK_set:
                        if x * y not in HK_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
        
        is_normal = True
        if is_subgroup:
            # Check normality condition: g * x * g^-1 in HK for all g in G, x in HK
            for g in G.elements:
                for x in HK_set:
                    if g * x * ~g not in HK_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        neg_q = not (is_subgroup and is_normal)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "¬Q: HK is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2